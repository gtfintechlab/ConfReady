import json
import logging
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request, stream_with_context
from flask_cors import CORS
from process_file import process_file
from process_file_markdown import process_file as process_file_markdown

load_dotenv()  

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
status_updates: List[str] = []

# ── Logging config ─────────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger("server")

# ── Virtual‑env bootstrap ──────────────────────────────────────────────────────
def ensure_marker_env() -> str:
    """Return path to marker_env’s python, creating the venv + deps the first time."""
    env_dir = Path.cwd() / "marker_env"
    python_exec = env_dir / "bin" / "python3"

    if env_dir.exists():
        log.debug("marker_env already exists → %s", env_dir)
        return str(python_exec)

    log.info("Creating marker_env virtualenv at %s …", env_dir)
    subprocess.check_call([sys.executable, "-m", "venv", str(env_dir)])
    subprocess.check_call([str(python_exec), "-m", "pip", "install", "--upgrade", "pip"])

    pkgs = [
        "marker-pdf==1.8.2",
        "aiohttp>=3.7,<4",
        "jinja2>=3.0",
        "requests>=2.25",
        "rich>=10.2",
        "python-dotenv>=1.0",
        "together"
    ]
    log.info("⬇ Installing %s", pkgs)
    subprocess.check_call([str(python_exec), "-m", "pip", "install", *pkgs])

    log.info("marker_env ready.")
    return str(python_exec)

# ── Extract archives ───────────────────────────────────────────────────
def extract_files(archive_path: str, temp_dir: str) -> List[str]:
    """Return list of .tex files extracted from a zip / tar.gz."""
    log.debug("Extracting %s → %s", archive_path, temp_dir)
    tex_files: List[str] = []

    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path) as z:
            z.extractall(temp_dir)
            tex_files = [
                os.path.join(temp_dir, f) for f in z.namelist() if f.endswith(".tex")
            ]

    elif archive_path.endswith(".tar.gz"):
        with tarfile.open(archive_path, "r:gz") as t:
            t.extractall(temp_dir)
            tex_files = [
                os.path.join(temp_dir, m.name)
                for m in t.getmembers()
                if m.isfile() and m.name.endswith(".tex")
            ]

    log.debug("Found %d .tex files: %s", len(tex_files), tex_files)
    return tex_files

# ── Merge .tex files ───────────────────────────────────────────────────
def merge_tex_files(tex_files: List[str], combined_path: str) -> str:
    """Concatenate multiple .tex files → single .tex"""
    log.debug("Merging %d .tex files → %s", len(tex_files), combined_path)
    with open(combined_path, "w") as out:
        for p in tex_files:
            with open(p) as f:
                out.write(f.read() + "\n")
    return combined_path

# ── Helper: run marker_runner with streaming output ────────────────────────────
def run_marker_runner(pdf_path: str, output_dir: str, python_exec: str) -> dict:
    """
    Launch marker_runner.py with live logging and return its JSON payload.
    Raises RuntimeError on non‑zero exit or bad JSON.
    """
    marker_runner = os.path.join(os.path.dirname(__file__), "marker_runner.py")
    cmd = [python_exec, marker_runner, pdf_path, output_dir]

    logging.info("marker_runner command: %s", " ".join(cmd))
    t0 = time.time()

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    stdout_lines = []
    for line in proc.stdout:
        stdout_lines.append(line)
        sys.stdout.write("marker ▶ " + line)

    proc.wait()
    elapsed = time.time() - t0
    logging.info("marker_runner finished in %.1fs (exit %s)", elapsed, proc.returncode)

    if proc.returncode != 0:
        raise RuntimeError(f"marker_runner.py failed with exit code {proc.returncode}")

    # Try to extract the last valid JSON line
    json_line = None
    for line in reversed(stdout_lines):
        stripped = line.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            json_line = stripped
            break

    if not json_line:
        raise RuntimeError(f"Could not parse marker_runner output as JSON:\n{''.join(stdout_lines)}")

    try:
        return json.loads(json_line)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to decode JSON from marker_runner output:\n{json_line}") from e


# ── Flask routes ───────────────────────────────────────────────────────────────
@app.route("/api/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files.get("file")
    if not uploaded_file or uploaded_file.filename == "":
        return jsonify({"error": "No file provided"}), 400

    log.info("📥  Received %s (%d bytes)", uploaded_file.filename, len(uploaded_file.read()))
    uploaded_file.seek(0)  # rewind after peek

    start = time.time()
    prompt_dict_choice = request.form.get("prompt_dict_choice", "acl")
    processed: Dict = {}

    
    if prompt_dict_choice == "acl":
        os.environ["SECTION_NAME_INSTRUCTION"] = (
            'Return a JSON object with exactly one field named "section name", '
            'whose value is exactly one of the section titles as it appears in the .tex. '
            'If no section applies, return {"section name":"None"}. '
            "Do not invent section names."
        )

    try:
        fname = uploaded_file.filename.lower()

        # ── ZIP / TAR.GZ ────────────────────────────────────────────────────
        if fname.endswith((".zip", ".tar.gz")):
            temp_path = os.path.join(tempfile.gettempdir(), fname)
            uploaded_file.save(temp_path)

            tmp_dir = tempfile.mkdtemp()
            try:
                tex_files = extract_files(temp_path, tmp_dir)
                merged = merge_tex_files(tex_files, os.path.join(tmp_dir, "merged.tex"))
                processed = process_file(merged, prompt_dict_choice)
            finally:
                shutil.rmtree(tmp_dir, ignore_errors=True)

        # ── Plain .tex ─────────────────────────────────────────────────────
        elif fname.endswith(".tex"):
            temp_path = os.path.join(tempfile.gettempdir(), fname)
            uploaded_file.save(temp_path)
            processed = process_file(temp_path, prompt_dict_choice)

        # ── PDF ────────────────────────────────────────────────────────────
        elif fname.endswith(".pdf"):
            tmp_in = tempfile.mkdtemp()
            tmp_out = tempfile.mkdtemp()
            try:
                pdf_path = os.path.join(tmp_in, fname)
                uploaded_file.save(pdf_path)
                marker_py = ensure_marker_env()
                result = run_marker_runner(pdf_path, tmp_out, marker_py)

                md_path = result.get("markdown_path")
                if not md_path or not os.path.exists(md_path):
                    return jsonify({"error": "PDF→Markdown conversion failed."}), 500

                processed = process_file_markdown(md_path)
            finally:
                shutil.rmtree(tmp_in, ignore_errors=True)
                shutil.rmtree(tmp_out, ignore_errors=True)

        else:
            return (
                jsonify({"error": "Unsupported file type; must be zip/tar.gz/tex/pdf."}),
                400,
            )

        processed["time_taken"] = f"{time.time() - start:.2f} s"
        return jsonify(processed), 200

    except Exception as exc:
        log.exception("Unexpected error during upload")
        return jsonify({"error": str(exc)}), 500

# ── SSE status feed ────────────────────────────────────────────────
@app.route("/api/upload/status", methods=["GET"])
def upload_status():
    def event_stream():
        for s in status_updates:
            yield f"data: {s}\n\n"
        status_updates.clear()

    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

@app.route("/api/upload/status/update", methods=["POST"])
def status_update():
    msg = request.json.get("status")
    if msg:
        status_updates.append(msg)
    return "", 204

@app.route("/api/helloworld")
def hello_world():
    return "Hello World!"

# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    log.info("Starting Flask on 0.0.0.0:%d", port)
    app.run(host="0.0.0.0", port=port, debug=False)
