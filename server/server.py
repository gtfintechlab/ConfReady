from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import json
import os
import tempfile
import re
from pdftitle import get_title_from_file
import spacy
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)

import re

def extract_authors_with_spacy(text):
    doc = nlp(text[:3000])
    authors = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')
    emails = email_pattern.findall(text)
    return {"authors": authors, "emails": emails}

def extract_metadata_authors(metadata):
    authors = metadata.get('/Author', '').split(',')
    return [author.strip() for author in authors if author]

def process_pdf(file):
    try:
        title = get_title_from_file(file)
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            metadata = pdf_reader.metadata

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Extract authors from metadata and text
            metadata_authors = extract_metadata_authors(metadata)

            links = []

            for page in pdf_reader.pages:
                annotations = page.get_object().get('/Annots', [])
                links += [
                    link.get_object().get('/A', {}).get('/URI')
                    for link in annotations if link.get_object().get('/Subtype') == '/Link'
                ]

            links = [link for link in links if link]

            spacy_nlp = extract_authors_with_spacy(text)

            return {"title": title, "links": links, "spacy": spacy_nlp}

    except Exception as e:
        return {"error": str(e)}

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
    result = process_pdf(temp_file_path)

    if 'error' in result:
        return jsonify({'error': result['error']})
    else:
        return jsonify(result)

@app.route("/api", methods=["GET"])
def hello_world():
    return jsonify({
        'message': 'Hello World'
    })

if __name__ == "__main__":
    app.run(debug=True, port=8080)
