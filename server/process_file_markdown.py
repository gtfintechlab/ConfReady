# -*- coding: utf-8 -*-
from collections import OrderedDict
import json
import os
import re
import pandas as pd
import time
from together import Together
from typing import List
from acl_checklist_prompts import generate_prompt_dict_acl
from neurips_a_checklist_prompts import generate_prompt_dict_neurips
from neurips_b_checklist_prompts import generate_prompt_dict_neurips_b
from llama_index.core import get_response_synthesizer
import logging
from llama_index.core.schema import IndexNode, TextNode, NodeRelationship, RelatedNodeInfo
from llama_index.llms.openai import OpenAI
import nest_asyncio
import requests
nest_asyncio.apply()
import json_repair
import datetime
import tempfile

from dotenv import load_dotenv
load_dotenv()

togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
client = Together(api_key=togetherai_api_key)

import openai
openai.api_key = openai_api_key
client = openai.OpenAI(api_key=openai_api_key)


def send_update(message):
    """
    Sending updates to the frontend about progress through the backend.
    """
    update_url = 'http://localhost:8080/api/upload/status/update'
    if update_url:
        try:
            requests.post(update_url, json={'status': message})
        except Exception as e:
            print(f"Failed to send update: {e}")


def process_file(filename):
    """Process Markdown files for LLM evaluation"""

    send_update(f"Started processing: {os.path.basename(filename)}")

    def read_markdown_doc(filename):
        """Reads Markdown file content"""
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()

    md_content = read_markdown_doc(filename)

    # Make the prompt even more explicit for the LLM
    prompt_instruction = (
        "If the the answer is 'YES', provide the section name.\n"
        "If the answer is 'NO' or 'NOT APPLICABLE', then output nothing.\n"
        "Provide a step by step justification for the answer.\n"
        "Respond with ONLY a valid JSON object with the keys 'answer', 'section name', and 'justification'. "
        "If the information isn't present, use 'unknown' as the value."
    )
    prompt_instruction_A3 = prompt_instruction

    prompt_dict = generate_prompt_dict_acl(prompt_instruction, prompt_instruction_A3, combined_node_id=None)

    results = {}
    query_keys = [
        "A1", "A2", "A3", "B1", "B2", "B3", "B4", "B5", "B6",
        "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4", "D5"
    ]

    for q_key in query_keys:
        results[q_key] = {
            "answer": "UNKNOWN",
            "section name": "UNKNOWN",
            "justification": "UNKNOWN",
            "raw_response": "",
            "json_response": {}
        }

    responses_dir = os.path.join(tempfile.gettempdir(), "markdown_responses")
    os.makedirs(responses_dir, exist_ok=True)
    responses_filename = os.path.join(responses_dir, f"{os.path.basename(filename)}_responses.txt")

    response_lines = [
        f"Processing started: {datetime.datetime.now().isoformat()}",
        f"Source paper: {filename}",
        "-" * 80
    ]

    MAX_RETRIES = 3
    RETRY_DELAY = 10

    def parse_json_response(raw_response):
        """Robust JSON parsing with multiple fallback strategies"""
        cleaned = re.sub(r'```(?:json)?\s*', '', raw_response, flags=re.IGNORECASE)
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        try:
            return json_repair.loads(cleaned)
        except Exception:
            pass

        try:
            start = cleaned.find('{')
            end = cleaned.rfind('}') + 1
            if start != -1 and end != -1 and end > start:
                return json.loads(cleaned[start:end])
        except Exception:
            pass

        return {
            "answer": "PARSE_ERROR",
            "section name": "PARSE_ERROR",
            "justification": f"Failed to parse: {raw_response[:100]}..."
        }

    for q_key in query_keys:
        send_update(f"Evaluating {q_key}")
        prompt = (
            "### DOCUMENT TEXT ###\n"
            f"{md_content}\n\n"
            "### QUESTION ###\n"
            f"{prompt_dict[q_key]}\n\n"
        )

        response_lines.append(f"\n{'=' * 80}")
        response_lines.append(f"QUERY: {prompt_dict[q_key]}")
        response_lines.append(f"{'=' * 80}\n")

        success = False
        raw_response = ""

        for attempt in range(1, MAX_RETRIES + 1):
            send_update(f"Sending prompt for {q_key} (attempt {attempt}/{MAX_RETRIES})")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Respond with ONLY valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    response_format={"type": "json_object"},
                )

                raw_response = response.choices[0].message.content.strip()
                response_lines.append(f"RESPONSE (attempt {attempt}):\n{raw_response}\n")

                parsed = parse_json_response(raw_response)

                valid_keys = {'answer', 'section name', 'justification'}
                if not all(key in parsed for key in valid_keys):
                    if attempt < MAX_RETRIES:
                        forceful_prompt = (
                            prompt +
                            "\n\nYour last response was not valid JSON or was missing required keys. "
                            "Respond with ONLY a valid JSON object with the keys 'answer', 'section name', "
                            "and 'justification'. Do not include any other text, markdown, or explanation."
                        )
                        response_lines.append("Retrying with more forceful prompt.")
                        prompt = forceful_prompt
                        raise ValueError("Missing required keys in response")
                    else:
                        raise ValueError("Missing required keys in response")

                results[q_key] = {
                    "answer": parsed.get("answer", "UNKNOWN").upper(),
                    "section name": parsed.get("section name", "UNKNOWN"),
                    "justification": parsed.get("justification", "UNKNOWN"),
                    "raw_response": raw_response,
                    "json_response": parsed
                }

                send_update(f"{q_key} processed successfully")
                success = True
                break

            except Exception as e:
                error_msg = f"ERROR on {q_key} attempt {attempt}: {str(e)}"
                response_lines.append(error_msg)
                send_update(f"Error on {q_key} (attempt {attempt}): {str(e)}")
                results[q_key]["raw_response"] = error_msg

                if "400" in str(e) or "422" in str(e):
                    response_lines.append("Skipping retries due to client error")
                    break

                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * attempt)

            finally:
                with open(responses_filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(response_lines))

        if not success:
            fail_msg = f"FAILED after {MAX_RETRIES} attempts"
            response_lines.append(fail_msg)
            results[q_key]["raw_response"] = fail_msg
            send_update(f"Failed to process {q_key} after {MAX_RETRIES} attempts")

    send_update(f"Finished processing: {os.path.basename(filename)}")
    print(f"Response log saved: {responses_filename}")
    return results
