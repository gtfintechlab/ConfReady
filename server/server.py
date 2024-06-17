import os
from dotenv import load_dotenv
import pdfplumber
import json
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

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

def prompt_discuss_limitations(parsedText):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    Your task is to analyze the provided research paper and answer the following question from the checklist: "Did you discuss the limitations of your work?"

    If the answer is YES, provide the section number. If the answer is NO, provide a justification.

    Research Paper: ```{parsedText}```

    Your response should be in JSON format with the keys "answer" (YES/NO) and "justification" (if YES, the section number; if NO, the justification).
    '''
    return ask_llm(prompt)

def prompt_discuss_potential_risks(parsedText):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    Your task is to analyze the provided research paper and answer the following question from the checklist: "Did you discuss any potential risks of your work?"

    If the answer is YES, provide the section number. If the answer is NO, provide a justification.

    Research Paper: ```{parsedText}```

    Your response should be in JSON format with the keys "answer" (YES/NO) and "justification" (if YES, the section number; if NO, the justification).
    '''
    return ask_llm(prompt)

def prompt_summarize_claims(parsedText):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    Your task is to analyze the provided research paper and answer the following question from the checklist: "Do the abstract and introduction summarize the paper’s main claims?"

    If the answer is YES, provide the section number. If the answer is NO, provide a justification.

    Research Paper: ```{parsedText}```

    Your response should be in JSON format with the keys "answer" (YES/NO) and "justification" (if YES, the section number; if NO, the justification).
    '''
    return ask_llm(prompt)

def prompt_cite_creators(parsedText):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    Your task is to analyze the provided research paper and answer the following question from the checklist: "Did you cite the creators of artifacts you used?"

    If the answer is YES, provide the section number. If the answer is NO, provide a justification.

    Research Paper: ```{parsedText}```

    Your response should be in JSON format with the keys "answer" (YES/NO) and "justification" (if YES, the section number; if NO, the justification).
    '''
    return ask_llm(prompt)

def prompt_discuss_license(parsedText):
    prompt = f'''
    You are an assistant to a researcher who intends to submit their research paper to the ACL Conference. To avoid desk rejection, the researcher wants to ensure their paper meets the benchmarks set by the Responsible NLP Research Checklist.

    Your task is to analyze the provided research paper and answer the following question from the checklist: "Did you discuss the license or terms for use and/or distribution of any artifacts?"

    If the answer is YES, provide the section number. If the answer is NO, provide a justification.

    Research Paper: ```{parsedText}```

    Your response should be in JSON format with the keys "answer" (YES/NO) and "justification" (if YES, the section number; if NO, the justification).
    '''
    return ask_llm(prompt)

# Add more function questions as needed

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

    parsed_text = parsed_result["text"]

    responses = {
        "Discuss Limitations": json.loads(prompt_discuss_limitations(parsed_text)),
        "Discuss Potential Risks": json.loads(prompt_discuss_potential_risks(parsed_text)),
        "Summarize Claims": json.loads(prompt_summarize_claims(parsed_text)),
        "Cite Creators": json.loads(prompt_cite_creators(parsed_text)),
        "Discuss License": json.loads(prompt_discuss_license(parsed_text)),
        # Add more question responses as needed
    }

    return jsonify(responses)

@app.route("/api", methods=["GET"])
def hello_world():
    return jsonify({
        'message': 'Hello World'
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
