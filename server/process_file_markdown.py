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
togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
client = Together(api_key= togetherai_api_key)
import openai
import tempfile

from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key
client = openai.OpenAI(api_key=openai_api_key)

def process_file(filename):
    """Process Markdown files for LLM evaluation"""
    
    def read_markdown_doc(filename):
        """Reads Markdown file content"""
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    
    md_content = read_markdown_doc(filename)

    
    # Make the prompt even more explicit for the LLM
    prompt_instruction = f"""If the the answer is 'YES', provide the section name.\nIf the answer is 'NO' or 'NOT APPLICABLE', then output nothing.\nProvide a step by step justification for the answer.\nRespond with ONLY a valid JSON object with the keys 'answer', 'section name', and 'justification'. If the information isn't present, use 'unknown' as the value."""

    prompt_instruction_A3 = f"""If the the answer is 'YES', provide the section name.\nIf the answer is 'NO' or 'NOT APPLICABLE', then output nothing.\nProvide a step by step justification for the answer.\nRespond with ONLY a valid JSON object with the keys 'answer', 'section name', and 'justification'. If the information isn't present, use 'unknown' as the value."""
    # Generate prompts
    # FIX: Provide a default value for combined_node_id as required by generate_prompt_dict_acl
    prompt_dict = generate_prompt_dict_acl(prompt_instruction, prompt_instruction_A3, combined_node_id=None)
    results = {}
    query_keys = ["A1", "A2", "A3", "B1", "B2", "B3", "B4", "B5", "B6", 
                 "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4", "D5"]
    
    for q_key in query_keys:
        results[q_key] = {
            "answer": "UNKNOWN",
            "section name": "UNKNOWN",
            "justification": "UNKNOWN",
            "raw_response": "",
            "json_response": {}
        }

    # Create responses directory
    responses_dir = os.path.join(tempfile.gettempdir(), "markdown_responses")
    os.makedirs(responses_dir, exist_ok=True)
    responses_filename = os.path.join(
        responses_dir,
        f"{os.path.basename(filename)}_responses.txt"
    )
    
    response_lines = [
        f"Processing started: {datetime.datetime.now().isoformat()}",
        f"Source paper: {filename}",
        "-" * 80
    ]

    MAX_RETRIES = 3
    RETRY_DELAY = 10
    
    def parse_json_response(raw_response):
        """Robust JSON parsing with multiple fallback strategies"""
        # Clean common non-JSON artifacts
        cleaned = re.sub(r'```(?:json)?\s*', '', raw_response, flags=re.IGNORECASE)
        cleaned = cleaned.strip()
        
        # Try direct parsing first
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        # Try JSON repair
        try:
            return json_repair.loads(cleaned)
        except Exception:
            pass
        
        # Extract first JSON-like substring
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
        # Structure prompt to clearly separate document from question
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
            try:
                # print(f"Sending {q_key} request (attempt {attempt}/{MAX_RETRIES})...")
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
                
                # Parse and validate response
                parsed = parse_json_response(raw_response)
                
                # Validate response structure
                valid_keys = {'answer', 'section name', 'justification'}
                if not all(key in parsed for key in valid_keys):
                    # Fallback: try a more forceful prompt if not last attempt
                    if attempt < MAX_RETRIES:
                        forceful_prompt = (
                            prompt +
                            "\n\nYour last response was not valid JSON or was missing required keys. Respond with ONLY a valid JSON object with the keys 'answer', 'section name', and 'justification'. Do not include any other text, markdown, or explanation."
                        )
                        response_lines.append("Retrying with more forceful prompt.")
                        prompt = forceful_prompt
                        raise ValueError("Missing required keys in response")
                    else:
                        raise ValueError("Missing required keys in response")
                
                # Update results
                results[q_key] = {
                    "answer": parsed.get("answer", "UNKNOWN").upper(),
                    "section name": parsed.get("section name", "UNKNOWN"),
                    "justification": parsed.get("justification", "UNKNOWN"),
                    "raw_response": raw_response,
                    "json_response": parsed
                }
                
                success = True
                break
                
            except Exception as e:
                error_msg = f"ERROR on {q_key} attempt {attempt}: {str(e)}"
                # print(error_msg)
                response_lines.append(error_msg)
                
                # Store error in results
                results[q_key]["raw_response"] = error_msg
                
                if "400" in str(e) or "422" in str(e):
                    response_lines.append("Skipping retries due to client error")
                    break
                    
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY * attempt)
            finally:
                # Always save intermediate results
                with open(responses_filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(response_lines))

        if not success:
            fail_msg = f"FAILED after {MAX_RETRIES} attempts"
            response_lines.append(fail_msg)
            results[q_key]["raw_response"] = fail_msg

    print(f"Response log saved: {responses_filename}")
    return results