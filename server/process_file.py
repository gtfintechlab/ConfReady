# -*- coding: utf-8 -*-
"""
ConfReady Document Processing Module

This module processes LaTeX documents and generates responses for various conference checklists.

DEV_MODE Usage:
    Set the environment variable DEV_MODE=true to process only the first 3 questions
    for faster testing and development.
    
    Example:
        export DEV_MODE=true
        python process_file.py
    
    This will process:
    - ACL: A1, A2, A3
    - NeurIPS: 1, 2, 3  
    - NeurIPS D&B: 1a, 1b, 1c
"""

from collections import OrderedDict
import json
import os
import re
from together import Together
from typing import List
from acl_checklist_prompts import generate_prompt_dict_acl
from neurips_a_checklist_prompts import generate_prompt_dict_neurips
from neurips_b_checklist_prompts import generate_prompt_dict_neurips_b
from llama_index.core import get_response_synthesizer
from llama_index.core.postprocessor import LLMRerank
from sklearn.metrics.pairwise import cosine_similarity
import bm25s
import logging
from openai import OpenAI
import numpy as np
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.query_engine import MultiStepQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.openai import OpenAI
import nest_asyncio
import requests
nest_asyncio.apply()
from llama_index.core.schema import IndexNode, TextNode, NodeRelationship, RelatedNodeInfo
from collections import defaultdict
import json_repair
import time

# Current github issue here (rerank is still useful) :
# https://github.com/run-llama/llama_index/issues/11093
class SafeLLMRerank:
    def __init__(self, choice_batch_size=5, top_n=2):
        self.choice_batch_size = choice_batch_size
        self.top_n = top_n
        self.reranker = LLMRerank(
            choice_batch_size=choice_batch_size,
            top_n=top_n,
        )

    def postprocess_nodes(self, nodes, query_bundle):
        try:
            return self.reranker.postprocess_nodes(nodes, query_bundle)
        except Exception as e:
            print(f"Rerank issue: {e}")
            return nodes

# Get Environmental Variables
togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Development Mode - Set to True to process only first 3 questions for faster testing
DEV_MODE = False

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

def process_file(filename, prompt_dict_choice):
        """Load Data and Setup"""
        class SectionNumberer:
            """
            When converting tex files to pdfs in overleaf, sections become numbered before appendix.
            In the appendix, they are num
            and during appendix they are lettered.
            This function mimic that behavior by converting the sections
            """
            def __init__(self):
                self.section_count = 0
                self.subsection_count = 0
                self.alpha_section_count = 0
                self.bibliography_found = False  # Flag to track if bibliography has been found

            def replace_heading(self, match):
                command = match.group(1)  # 'section', 'subsection', or 'bibliography'
                content = match.group(2)  # Title inside the braces

                # If bibliography command is encountered, switch to alphabetic numbering
                if command == 'bibliography':
                    self.bibliography_found = True
                    return match.group(0)  # Optionally return the bibliography line unchanged

                # Process sections and subsections based on the numbering mode
                if self.bibliography_found:
                    if command == 'section':
                        self.alpha_section_count += 1
                        section_label = chr(64 + self.alpha_section_count)  # Convert to letters A, B, C, etc.
                        self.subsection_count = 0  # Reset subsection count for new section
                        return f"\\section{{{section_label} {content}}}"
                    elif command == 'subsection':
                        self.subsection_count += 1
                        subsection_label = f"{chr(64 + self.alpha_section_count)}.{self.subsection_count}"
                        return f"\\subsection{{{subsection_label} {content}}}"
                else:
                    if command == 'section':
                        self.section_count += 1
                        self.subsection_count = 0  # Reset subsection count
                        return f"\\section{{{self.section_count} {content}}}"
                    elif command == 'subsection':
                        self.subsection_count += 1
                        return f"\\subsection{{{self.section_count}.{self.subsection_count} {content}}}"

            def number_sections(self, tex_content):
                # Regex to find all section, subsection, or bibliography commands
                pattern = re.compile(r"\\(section|subsection|bibliography)\{([^}]*)\}")
                processed_content = pattern.sub(self.replace_heading, tex_content)
                return processed_content

        def extract_text_and_captions_table(latex_string):
            """
            Remove tables, but keep the table captions (they are numbered).
            """
            # Regex to find all table environments (both \begin{table*} and \begin{table})
            table_pattern = re.compile(r'(\\begin\{table\*?\}.*?\\end\{table\*?\})', re.DOTALL)

            # Split the text at each table environment
            parts = table_pattern.split(latex_string)

            result_parts = []
            caption_counter = 1

            for part in parts:
                if table_pattern.match(part):
                    # Find the caption within this table
                    caption_match = re.search(r'\\caption\{([^}]*)\}', part)
                    if caption_match:
                        caption_text = caption_match.group(1)
                        result_parts.append(f'Table {caption_counter} Description: {caption_text}. End Table {caption_counter} Description.')
                        caption_counter += 1
                else:
                    result_parts.append(part)

            # Combine the extracted text parts and captions
            combined_text = ' '.join(result_parts)

            # Clean up any extra spaces introduced
            clean_text = re.sub(r'\s+', ' ', combined_text).strip()

            return clean_text

        def extract_text_and_captions_figure(latex_string):
            """
            Remove figures, but keep the figure captions (they are numbered).
            """

            # Regex to find all figure environments (both \begin{figure*} and \begin{figure})
            table_pattern = re.compile(r'(\\begin\{figure\*?\}.*?\\end\{figure\*?\})', re.DOTALL)

            # Split the text at each figure environment
            parts = table_pattern.split(latex_string)

            result_parts = []
            caption_counter = 1

            for part in parts:
                if table_pattern.match(part):
                    # Find the caption within this figure
                    caption_match = re.search(r'\\caption\{([^}]*)\}', part)
                    if caption_match:
                        caption_text = caption_match.group(1)
                        result_parts.append(f'Figure {caption_counter} Description: {caption_text}. End Figure {caption_counter} Description.')
                        caption_counter += 1
                else:
                    result_parts.append(part)

            # Combine the extracted text parts and captions
            combined_text = ' '.join(result_parts)

            # Clean up any extra spaces introduced
            clean_text = re.sub(r'\s+', ' ', combined_text).strip()

            return clean_text
        
        def read_latex_doc(filename):
            with open(filename, 'r') as file:
                tex_content = file.read()

            def extract_title(tex_content):
                """
                This is meant to go to the source in all nodes
                """

                # Regex pattern to match text within \title{...}
                pattern = re.compile(r'\\title\{([^}]*)\}')
                result = pattern.search(tex_content)
                return result.group(1) if result else ''

            def remove_document_tags(tex_content):
                """
                Remove \begin{document} and \end{document} from LaTeX content.
                """
                tex_content = re.sub(r'\\begin{document}', '', tex_content)
                tex_content = re.sub(r'\\end{document}', '', tex_content)
                return tex_content

            def start_with_abstract(tex_content):
                """
                Keep only the content starting from \begin{abstract}.
                """
                match = re.search(r'\\begin{abstract}', tex_content)
                if match:
                    tex_content = tex_content[match.start():]
                return tex_content

            def remove_comments(tex_content):
                """
                Remove commented lines from LaTeX content while preserving original line endings.
                """
                lines = re.split('(\r\n|\r|\n)', tex_content)  # Capture the line endings
                uncommented_lines = [line for line in lines if not line.strip().startswith('%') and not re.match(r'(\r\n|\r|\n)', line)]
                line_endings = [line for line in lines if re.match(r'(\r\n|\r|\n)', line)]

                # Reconstruct the text preserving line endings
                uncommented_text = ''.join(uncommented_lines + line_endings)
                return uncommented_text

            def add_spaces_around_commands(text, commands):
                for command in commands:
                    # Create a regular expression pattern for each command, including optional *
                    pattern = rf'(\\{command}\*?\{{.*?\}})'

                    # Add spaces around each matched command pattern
                    text = re.sub(pattern, r' \1 ', text)

                # Remove any duplicate spaces that may have been introduced
                text = re.sub(r'\s+', ' ', text).strip()

                return text

            def remove_consecutive_occurrences(line):
                # Use a regular expression to replace consecutive occurrences of %%
                # Some people use multiple line strings
                return re.sub(r'(%%)+', r'\1', line)

            def number_sections(tex_content):
                section_count = 0
                appendix_mode = False
                alpha_section_count = 0
                subsection_count = 0  # Initialize subsection count

                def replace_heading(match):
                    nonlocal section_count, alpha_section_count, appendix_mode, subsection_count
                    heading_type = match.group(1)  # Determine whether it's 'section' or 'subsection'
                    heading_content = match.group(2)  # Capture the title inside the braces

                    if "\\appendix" in heading_content:
                        appendix_mode = True
                        return match.group(0)  # Return the original line

                    if heading_type == 'section':
                        if appendix_mode:
                            alpha_section_count += 1
                            section_label = chr(64 + alpha_section_count)
                            subsection_count = 0  # Reset subsection count
                            return f"\\section{{{section_label}. {heading_content}}}"
                        else:
                            section_count += 1
                            subsection_count = 0  # Reset subsection count
                            return f"\\section{{{section_count}. {heading_content}}}"
                    elif heading_type == 'subsection':
                        if appendix_mode:
                            subsection_count += 1
                            subsection_label = f"{chr(64 + alpha_section_count)}.{subsection_count}"
                            return f"\\subsection{{{subsection_label}. {heading_content}}}"
                        else:
                            subsection_count += 1
                            return f"\\subsection{{{section_count}.{subsection_count}. {heading_content}}}"

                # Regex to find all section and subsection commands
                pattern = re.compile(r"\\(section|subsection)\{([^}]*)\}")
                processed_content = pattern.sub(replace_heading, tex_content)
                return processed_content

            def split_sections(tex_content):
                # Split using lookahead to ensure \section starts a new chunk
                # This splits before each \section{...}
                chunks = re.split(r'(?=\\section\*?{[^}]*})', tex_content)

                # Initialize list to store properly combined chunks
                combined_chunks = []

                # Append the first chunk directly as it includes content before any \section
                if chunks and not chunks[0].startswith('\\section'):
                    combined_chunks.append(chunks.pop(0))

                # Remaining chunks should already start with \section
                combined_chunks.extend(chunks)

                return combined_chunks

            # Remove \begin{document} and \end{document}
            tex_content = remove_document_tags(tex_content)

            # List of LaTeX commands to handle that can add spaces where non exist. This is extremely important for LLMs to chunk.
            commands = ['footnote', 'href', 'textbf', 'section', 'section*', 'subsection', 'subsection*']

            tex_content = add_spaces_around_commands(tex_content, commands)

            # Remove most of table content except caption.
            tex_content = extract_text_and_captions_table(tex_content)

            # Remove most of table content except caption.
            tex_content = extract_text_and_captions_figure(tex_content)

            # Start with \begin{abstract}
            tex_content = start_with_abstract(tex_content)

            # Remove commented lines
            tex_content = remove_comments(tex_content)

            # Remove multiple line comments.
            tex_content = remove_consecutive_occurrences(tex_content)

            # Create an instance of SectionNumberer and process the LaTeX content
            numberer = SectionNumberer()
            tex_content = numberer.number_sections(tex_content)

            list_chunks = split_sections(tex_content)

            # Regex pattern to match strings starting with \section*{Acknowledgements} or \section{Acknowledgements} (case-insensitive)
            pattern = re.compile(r'\\section\*?\{acknowledgements\}', re.IGNORECASE)

            # Filter out items that match the pattern
            list_chunks = [chunk for chunk in list_chunks if not pattern.match(chunk)]

            # Replace \begin{abstract} with \section*{abstract}
            list_chunks[0] = list_chunks[0].replace('\\begin{abstract}', '\\section*{abstract}')

            # Replace \end{abstract} with an empty string
            list_chunks[0] = list_chunks[0].replace('\\end{abstract}', '')

            # Extract the title content
            title = extract_title(tex_content)

            return(list_chunks, tex_content, title)

        list_chunks, tex_content, title = read_latex_doc(filename)

        """## Parsing Documents into Text Chunks (Nodes)"""

        def extract_text(text):
            # Regex pattern to match text within curly braces for all specified cases
            pattern = re.compile(r'\\(?:begin|section\*?)\{([^}]*)\}')
            result = pattern.search(text)
            return result.group(1) if result else ''

        def check_license(node1):
            """
            This is just an experiment with metadata for licenses. Future work.
            """
            normalized_node = node1.lower().replace('-', ' ')
            if 'cc by nc 4.0' in normalized_node:
                return 'CC BY-NC 4.0'
            else:
                return ''

        # concatenate the names of node 0 and 1 (abstract and introduction) for A3
        node_ids = []

        base_nodes = []
        for chunk in list_chunks:
            node_id = extract_text(chunk)
            node_ids.append(node_id)
            base_nodes.append(TextNode(text=chunk, id_=node_id))
            #base_nodes.append(TextNode(text=chunk, id_=node_id, metadata = {'license': check_license(chunk)}))

        # Check if there are at least two node_ids to concatenate (for question A3)
        if len(node_ids) >= 2:
            combined_node_id = '/'.join(node_ids[:2])  # Concatenate the first two node_ids
        else:
            combined_node_id = None  # Handle cases where there are less than two node_ids

        # Adding section names and basic prompt instructions to each prompt
        section_names = []
        for node in base_nodes:
            section_names.append(node.id_)

        # Papers missing a limitations section are desk rejected
        # https://aclrollingreview.org/cfp
        if not any('Limitation' in section for section in section_names):
            A1_issue = 1
        else:
            A1_issue = 0

        # Join the node names with commas and the last one with 'and', all enclosed in single quotes
        quoted_names = [f"'{name}'" for name in section_names]
        section_names_text = ', '.join(quoted_names[:-1]) + ', and ' + quoted_names[-1]

        prompt_instruction = f"""If the the answer is 'YES', provide the section name.
        Only return valid section names which are {section_names_text}.
        If the answer is 'NO' or 'NOT APPLICABLE', then output nothing.
        Provide a step by step justification for the answer.
        Format your response as ONLY a JSON object with 'answer', 'section name', and 'justification' as the keys.
        If the information isn't present, use 'unknown' as the value."""

        prompt_instruction_A3 = f"""If the the answer is 'YES', provide the section name.
        Only return valid section names which are {section_names_text}.
        If the answer is 'NO' or 'NOT APPLICABLE', then output nothing.
        Provide a step by step justification for the answer.
        Format your response as a JSON object with 'answer', 'section name', and 'justification' as the keys.
        If the information isn't present, use 'unknown' as the value."""
        prompt_dict = generate_prompt_dict_acl(prompt_instruction, prompt_instruction_A3, section_names_text)
        if prompt_dict_choice == "acl":
                prompt_dict = generate_prompt_dict_acl(prompt_instruction, prompt_instruction_A3, combined_node_id)
        elif prompt_dict_choice == "neurips":
                prompt_dict = generate_prompt_dict_neurips(prompt_instruction, combined_node_id)
        elif prompt_dict_choice == "neurips_b":
                prompt_dict = generate_prompt_dict_neurips_b(prompt_instruction)

        CONTEXTUAL_RAG_PROMPT = """
        Given the document below, we want to explain what the chunk captures in the document.
        {WHOLE_DOCUMENT}
        Here is the chunk we want to explain:
        {CHUNK_CONTENT}
        Answer ONLY with a succinct explaination of the meaning of the chunk in the context of the whole document above.
        """

        # Function to generate prompts
        def generate_prompts(document: str, chunks: List[str], tex_content: str) -> List[str]:
            prompts = []
            for chunk in chunks:
                prompt = CONTEXTUAL_RAG_PROMPT.format(WHOLE_DOCUMENT=tex_content, CHUNK_CONTENT=chunk)
                prompts.append(prompt)
            return prompts
        
        prompts = generate_prompts(tex_content, list_chunks, tex_content)

        def generate_context(prompt: str):
            """
            Generates a contextual response based on the given prompt using the specified language model.
            Args:
            prompt (str): The input prompt to generate a response for.
            Returns:
            str: The generated response content from the language model.
            """

            client = Together(api_key = togetherai_api_key)
            response = client.chat.completions.create(
            model= "meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
            )
            return response.choices[0].message.content
    
        def generate_embeddings(input_texts: List[str], model_api_string: str) -> List[List[float]]:
            """
            Generate embeddings from Together python library.

            Args:
            input_texts: a list of string input texts.
            model_api_string: str. An API string for a specific embedding model of your choice.

            Returns:
            embeddings_list: a list of embeddings. Each element corresponds to the each input text.
            """

            client = Together(api_key = togetherai_api_key)

            outputs = client.embeddings.create(
            input= input_texts,
            model="togethercomputer/m2-bert-80M-32k-retrieval"
            )
            return [x.embedding for x in outputs.data]
    
        contextual_chunks = []
        for i in range(len(list_chunks)):
            context = generate_context(prompts[i]) + ' ' + list_chunks[i]
            contextual_chunks.append(context)
        contextual_embeddings = generate_embeddings(contextual_chunks, "togethercomputer/m2-bert-80M-32k-retrieval")

        def extract_text(text):
            # Regex pattern to match text within curly braces for all specified cases
            pattern = re.compile(r'\\(?:begin|section\*?)\{((?:[^\{\}]|\{[^\{\}]*\})+)\}')
            result = pattern.search(text)
            return result.group(1) if result else ''

        def check_license(node1):
            """
            This is just an experiment with metadata for licenses. Future work.
            """
            normalized_node = node1.lower().replace('-', ' ')
            if 'cc by nc 4.0' in normalized_node:
                return 'CC BY-NC 4.0'
            else:
                return ''

        prompt_dict = generate_prompt_dict_acl(prompt_instruction, prompt_instruction_A3, combined_node_id)

        def vector_retreival(query: str, top_k: int = 5, vector_index: np.ndarray = None) -> List[int]:
            """
            Retrieve the top-k most similar items from an index based on a query.
            Args:
            query (str): The query string to search for.
            top_k (int, optional): The number of top similar items to retrieve. Defaults to 5.
            index (np.ndarray, optional): The index array containing embeddings to search against. Defaults to None.
            Returns:
            List[int]: A list of indices corresponding to the top-k most similar items in the index.
            """

            query_embedding = generate_embeddings([query], 'togethercomputer/m2-bert-80M-32k-retrieval')[0]
            similarity_scores = cosine_similarity([query_embedding], vector_index)

            return list(np.argsort(-similarity_scores)[0][:top_k])
    
        # Create the BM25 model and index the corpus
        retriever = bm25s.BM25(corpus=contextual_chunks)
        retriever.index(bm25s.tokenize(contextual_chunks))

        def bm25_retreival(query: str, k : int, bm25_index) -> List[int]:
            """
            Retrieve the top-k document indices based on the BM25 algorithm for a given query.
            Args:
            query (str): The search query string.
            k (int): The number of top documents to retrieve.
            bm25_index: The BM25 index object used for retrieval.
            Returns:
            List[int]: A list of indices of the top-k documents that match the query.
            """

            results, scores = bm25_index.retrieve(bm25s.tokenize(query), k=k)

            return [contextual_chunks.index(doc) for doc in results[0]]
        

        def reciprocal_rank_fusion(*list_of_list_ranks_system, K=60):
            """
            Fuse rank from multiple IR systems using Reciprocal Rank Fusion.

            Args:
            * list_of_list_ranks_system: Ranked results from different IR system.
            K (int): A constant used in the RRF formula (default is 60).

            Returns:
            Tuple of list of sorted documents by score and sorted documents
            """
            # Dictionary to store RRF mapping
            rrf_map = defaultdict(float)

            # Calculate RRF score for each result in each list
            for rank_list in list_of_list_ranks_system:
                for rank, item in enumerate(rank_list, 1):
                    rrf_map[item] += 1 / (rank + K)

            # Sort items based on their RRF scores in descending order
            sorted_items = sorted(rrf_map.items(), key=lambda x: x[1], reverse=True)

            # Return tuple of list of sorted documents by score and sorted documents
            return sorted_items, [item for item, score in sorted_items]


        client = Together(api_key=togetherai_api_key)
        results = {}
        
        # Define query keys based on checklist type
        if prompt_dict_choice == "acl":
            all_query_keys = ["A1", "A2", "A3", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4", "D5"]
        elif prompt_dict_choice == "neurips":
            all_query_keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
        elif prompt_dict_choice == "neurips_b":
            all_query_keys = ["1a", "1b", "1c", "1d", "2a", "2b", "3a", "3b", "3c", "3d", "4a", "4b", "4c", "4d", "4e", "5a", "5b", "5c"]
        else:
            all_query_keys = ["A1", "A2", "A3", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4", "D5"]
        
        # Limit to first 3 questions in DEV_MODE
        if DEV_MODE:
            query_keys = all_query_keys[:3]  # Only process first 3 questions
            print(f"DEV_MODE enabled: Processing only first 3 questions ({', '.join(query_keys)})")
            send_update(f"DEV_MODE: Processing only first 3 questions ({', '.join(query_keys)})")
        else:
            query_keys = all_query_keys
            print(f"Processing all {len(query_keys)} questions for {prompt_dict_choice} checklist")
        


        
        # Initialize response log
        response_lines = [
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
        
        send_update("Starting contextual retrieval process")
        for q_key in query_keys:
            query = prompt_dict[q_key]
            send_update(f"Processing query: {q_key}")
            print(f"Processing query: {q_key}")

            # Initialize result entry
            results[q_key] = {
                "answer": "UNKNOWN",
                "section name": "UNKNOWN",
                "justification": "UNKNOWN",
                "raw_response": "",
                "json_response": {}
            }

            # Retrieve top-k results
            try:
                vector_topk = vector_retreival(query=query, top_k=10, vector_index=contextual_embeddings)
                bm_25_topk = bm25_retreival(query, 5, bm25_index=retriever)
                hybrid_top_k = reciprocal_rank_fusion(vector_topk, bm_25_topk)
                hybrid_top_k_docs = [contextual_chunks[index] for index in hybrid_top_k[1]]
            
                # Rerank 
                rerank_response = client.rerank.create(
                    model="Salesforce/Llama-Rank-V1",
                    query=query,
                    documents=hybrid_top_k_docs,
                    top_n=10
                )
                top_k_chunks = [hybrid_top_k_docs[result.index] for result in rerank_response.results]
                retrieved_chunks = '\n\n'.join(top_k_chunks)
                prompt = f"{query} Here is relevant information: {retrieved_chunks}."
            except Exception as e:
                error_msg = f"Retrieval error for {q_key}: {str(e)}"
                print(error_msg)

                continue
            success = False
            raw_response = ""
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    print(f"Sending {q_key} request (attempt {attempt}/{MAX_RETRIES})...")
                    response = client.chat.completions.create(
                        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
                        messages=[
                            {"role": "system", "content": "Respond with ONLY valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.0,
                        response_format={"type": "json_object"},
                    )
                    
                    raw_response = response.choices[0].message.content.strip()
                    print(raw_response)

                    
                    # Parse and validate response
                    parsed = parse_json_response(raw_response)
                    
                    # Update results
                    results[q_key] = {
                        "answer": parsed.get("answer", "UNKNOWN").upper(),
                        "section name": parsed.get("section name", "UNKNOWN"),
                        "justification": parsed.get("justification", "UNKNOWN")
                    }
                    
                    success = True
                    break
                    
                except Exception as e:
                    error_msg = f"ERROR on {q_key} attempt {attempt}: {str(e)}"
                    print(error_msg)

                    if "400" in str(e) or "422" in str(e):
                        break
                        
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY * attempt)
            
            if not success:
                fail_msg = f"FAILED after {MAX_RETRIES} attempts"

                results[q_key]["raw_response"] = fail_msg


        send_update("Contextual retrieval process complete")
        return results