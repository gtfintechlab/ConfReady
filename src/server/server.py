import json
import logging
import os
import subprocess
import tempfile

import pdfplumber
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    # Save the uploaded file to a temporary location
    temp_file_path = os.path.join(tempfile.gettempdir(), file.filename)
    file.save(temp_file_path)
    logging.info(f"File saved to {temp_file_path}")

    # Call the external Python script
    try:
        # Outputs json to '../aclready/src/components/Sidebar/sample_output' + '.json'
        # This is .gitignored if you push to github. We should changed
        subprocess.run(
            ["python", "process_file.py", temp_file_path],
            check=True,
            capture_output=True,
            text=True,
        )
        # temporary output (hardcoded for now)
        output_file_path = "../aclready/src/components/Sidebar/sample_output" + ".json"
        logging.info(f"Output JSON file saved to {output_file_path}")

        with open(output_file_path, "r") as json_file:
            data = json.load(json_file)

        return jsonify(data), 200
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing file: {e.stderr}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return jsonify({"message": "File processed successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=8080)
