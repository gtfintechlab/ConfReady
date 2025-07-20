import os
import sys
from pathlib import Path

from marker.util import assign_config
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.config.parser import ConfigParser
from marker.output import text_from_rendered

# ────────────────────────────────────────────────────────────────
# TogetherService inline definition
# ────────────────────────────────────────────────────────────────

import together

class TogetherService:
    def __init__(self, model="meta-llama/Llama-3-8b-chat-hf"):
        self.api_key = os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise EnvironmentError("Missing TOGETHER_API_KEY")
        together.api_key = self.api_key
        self.model = model

    def __call__(self, prompt: str, **kwargs) -> str:
        response = together.Complete.create(
            model=self.model,
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7
        )
        return response["output"]["choices"][0]["text"]

# ────────────────────────────────────────────────────────────────
# Input/output config
# ────────────────────────────────────────────────────────────────

print("LOADED FILE:", os.path.abspath(__file__), file=sys.stderr)

input_dir = "./PDFs/"
output_dir = "./output_md/"
os.makedirs(output_dir, exist_ok=True)

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

config = {
    "output_format": "markdown",
    "output_dir": output_dir,
    "languages": "en",
    "paginate_output": True,
    "use_llm": True,
}
config_parser = ConfigParser(config)
TOGETHER_CLASS_PATH = "confready.server.marker_together_service.TogetherService"

# Optional: register config for compatibility
assign_config(TOGETHER_CLASS_PATH, {
    "model": "meta-llama/Llama-3-8b-chat-hf"
})

# 🧠 The key fix — use the class *instance* not a string
llm_service = TOGETHER_CLASS_PATH

converter = PdfConverter(
    llm_service=TOGETHER_CLASS_PATH,
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer()
)

# ────────────────────────────────────────────────────────────────
# Conversion Functions
# ────────────────────────────────────────────────────────────────

def convert_single_pdf_to_markdown(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_md_path = os.path.join(output_dir, f"{Path(pdf_path).stem}.md")
    try:
        rendered = converter(pdf_path)
        text, _, _ = text_from_rendered(rendered)
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(text)
        return output_md_path
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}", file=sys.stderr)
        return None

def process_pdfs(input_path, output_base):
    for root, dirs, files in os.walk(input_path):
        relative_path = os.path.relpath(root, input_path)
        output_path = os.path.join(output_base, relative_path)
        os.makedirs(output_path, exist_ok=True)
        print(f"📂 Scanning: {root}")

        pdf_files = [file for file in files if file.lower().endswith(".pdf")]
        if not pdf_files:
            continue

        for file in pdf_files:
            input_pdf_path = os.path.join(root, file)
            output_md_path = os.path.join(output_path, f"{Path(file).stem}.md")

            print(f"🔄 Processing: {input_pdf_path} -> {output_md_path}")
            if os.path.exists(output_md_path):
                print(f"⏩ Skipping (already exists): {output_md_path}")
                continue

            try:
                rendered = converter(input_pdf_path)
                text, _, _ = text_from_rendered(rendered)

                with open(output_md_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"✅ Saved: {output_md_path}")

            except Exception as e:
                print(f"❌ Error processing {input_pdf_path}: {e}", file=sys.stderr)

# ────────────────────────────────────────────────────────────────
# CLI Entrypoint
# ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    process_pdfs(input_dir, output_dir)
