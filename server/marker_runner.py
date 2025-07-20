#!/usr/bin/env python3
"""
marker_runner.py
Converts a single PDF → Markdown using marker_full_patched.convert_single_pdf_to_markdown
and prints a one‑line JSON result so the parent process can parse it.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Dynamically add project root (one level up from "confready/")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# ── Logging setup ──────────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger("marker_runner")

log.info("RUNNING marker_runner.py from: %s", Path(__file__).resolve())

# ── 1) Load .env and ensure required keys are present ──────────────────────────
load_dotenv()  # silently ignore if .env missing
REQUIRED_KEYS: List[str] = ["TOGETHER_API_KEY"]

missing = [k for k in REQUIRED_KEYS if not os.getenv(k)]
if missing:
    err = f"Missing required env keys: {missing}"
    log.error(err)
    print(json.dumps({"error": err}))
    sys.exit(1)

# Inject keys into os.environ for downstream usage
for k in REQUIRED_KEYS:
    os.environ[k] = os.getenv(k)

# ── 2) Import heavy deps AFTER env is ready ────────────────────────────────────
try:
    from marker_full_patched import convert_single_pdf_to_markdown
except Exception as import_err:
    log.exception("Failed importing marker_full_patched")
    print(json.dumps({"error": str(import_err)}))
    sys.exit(1)

# ── 3) Helper ------------------------------------------------------------------
def convert(pdf_path: str, out_dir: str) -> str:
    log.info("🗎  Converting PDF → Markdown …")
    log.debug("pdf_path=%s  out_dir=%s", pdf_path, out_dir)
    md_path = convert_single_pdf_to_markdown(pdf_path, out_dir)
    log.info("✅  Conversion complete: %s", md_path)
    return md_path

# ── 4) CLI entrypoint ----------------------------------------------------------
def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python marker_runner.py <pdf_path> <output_dir>", file=sys.stderr)
        sys.exit(1)

    pdf_path, output_dir = sys.argv[1:3]

    try:
        md_path = convert(pdf_path, output_dir)
        if md_path:
            print(json.dumps({"markdown_path": md_path}))
        else:
            raise RuntimeError("convert_single_pdf_to_markdown returned None")
    except Exception as e:
        log.exception("PDF→Markdown failed")
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
