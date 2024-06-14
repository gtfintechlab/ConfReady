import pdfplumber
import json
import os
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

togetherai_api_key = os.environ.get('TOGETHERAI_API_KEY')
client_together = OpenAI(api_key=togetherai_api_key, base_url='https://api.together.xyz')

def parse_pdf(file_path):
    try:
        text = ""
        links = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
                for annot in page.annots:
                    if 'uri' in annot:
                        links.append(annot['uri'])
        
        return {
            "text": text,
            "links": links
        }
    except Exception as e:
        return {"error": str(e)}

def summarize_text(parsedText):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    First, summarize the provided research paper, which is delimited by triple backticks, in no more than 1500 tokens.

    Research Paper: ```{parsedText}```
    '''

    prompt_json = [{'role': 'user', 'content': prompt}]

    model_source = 'meta-llama'
    model_name = 'Llama-3-70b-chat-hf'
    model_str = f'{model_source}/{model_name}'

    chat_completion = client_together.chat.completions.create(
        model=model_str,
        messages=prompt_json,
        temperature=0,
        max_tokens=1500
    )

    return chat_completion.choices[0].message.content

def generate_prompt(summarizedText, question):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    Your task is to analyze the provided summary of the research paper and answer the following question from the checklist: "{question}"

    If the answer is YES, provide the section number. If the answer is NO, provide a justification.

    Research Paper Summary: ```{summarizedText}```

    Your response should be in JSON format with the keys "answer" (YES/NO) and "justification" (if YES, the section number; if NO, the justification).
    '''
    return prompt



def ask_llm(prompt):
    prompt_json = [{'role': 'user', 'content': prompt}]

    model_source = 'meta-llama'
    model_name = 'Llama-3-70b-chat-hf'
    model_str = f'{model_source}/{model_name}'

    chat_completion = client_together.chat.completions.create(
        model=model_str,
        messages=prompt_json,
        temperature=0,
        max_tokens=512
    )

    return chat_completion.choices[0].message.content

@app.route("/api/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join(tempfile.gettempdir(), file.filename)
    file.save(temp_file_path)

    # Process the PDF file with the saved path
    parsed_result = parse_pdf(temp_file_path)
    if 'error' in parsed_result:
        return jsonify({'error': parsed_result['error']})

    # Summarize the text to handle token limits
    summarized_text = summarize_text(parsed_result["text"])

    questions = [
        "Did you discuss the limitations of your work?",
        "Did you discuss any potential risks of your work?",
        "Do the abstract and introduction summarize the paper’s main claims?",
        "Did you cite the creators of artifacts you used?",
        "Did you discuss the license or terms for use and/or distribution of any artifacts?",
        "Did you discuss if your use of existing artifact(s) was consistent with their intended use?",
        "Did you discuss the steps taken to check whether the data contains any personal information?",
        "Did you provide documentation of the artifacts?",
        "Did you report relevant statistics like the number of examples, details of train/test/dev splits?",
        "Did you report the number of parameters in the models used, the total computational budget, and computing infrastructure used?",
        "Did you discuss the experimental setup, including hyperparameter search and best-found hyperparameter values?",
        "Did you report descriptive statistics about your results?",
        "If you used existing packages, did you report the implementation, model, and parameter settings used?",
        "Did you report the full text of instructions given to participants?",
        "Did you report information about how you recruited and paid participants?",
        "Did you discuss whether and how consent was obtained from people whose data you're using?",
        "Was the data collection protocol approved by an ethics review board?",
        "Did you report the basic demographic and geographic characteristics of the annotator population?",
        "Did you include information about your use of AI assistants?"
    ]

    responses = {}
    for question in questions:
        prompt = generate_prompt(summarized_text, question)
        response = ask_llm(prompt)
        responses[question] = json.loads(response)
    
    return jsonify(responses)


@app.route("/api", methods=["GET"])
def hello_world():
    return jsonify({
        'message': 'Hello World'
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
