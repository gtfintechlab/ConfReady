# -*- coding: utf-8 -*-

# remove this comment
from collections import OrderedDict
import argparse
import json
import os
import re

from acl_checklist_prompts import generate_prompt_dict_acl
from neurips_a_checklist_prompts import generate_prompt_dict_neurips
from neurips_b_checklist_prompts import generate_prompt_dict_neurips_b

from llama_index.core import get_response_synthesizer
from llama_index.core import QueryBundle
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import (
    SemanticSplitterNodeParser
)

from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.postprocessor import KeywordNodePostprocessor
from llama_index.core.postprocessor import LLMRerank

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

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.query_engine import MultiStepQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

import nest_asyncio
import requests

nest_asyncio.apply()

from llama_index.core.schema import IndexNode, TextNode, NodeRelationship, RelatedNodeInfo

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

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.query_engine import MultiStepQueryEngine
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.llms.openai import OpenAI

import nest_asyncio
import requests

nest_asyncio.apply()

from llama_index.core.schema import IndexNode, TextNode, NodeRelationship, RelatedNodeInfo

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

    ## Get Environmental Variables

    #togetherai_api_key = os.getenv('TOGETHERAI_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')

    """## Load Data and Setup"""

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

        send_update("Parsing Latex Information")

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
            send_update("Performing semantic chunking")
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

        return(list_chunks, title)

    list_chunks, title = read_latex_doc(filename)


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

    # Add relationships between nodes

    for i, node in enumerate(base_nodes):
        if i < len(base_nodes) - 1:
            next_node = base_nodes[i + 1]
            node.relationships[NodeRelationship.NEXT] = RelatedNodeInfo(
                node_id=next_node.id_
            )
        if i > 0:
            previous_node = base_nodes[i - 1]
            node.relationships[NodeRelationship.PREVIOUS] = RelatedNodeInfo(
                node_id=previous_node.id_
            )

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

    # ADD SECTION HALLUCINATION INSTRUCTION IF PRESENT IN ENV VAR  -----------------------------
    hallucination_warning = os.getenv("SECTION_NAME_INSTRUCTION", "")

    prompt_instruction_acl = hallucination_warning + f"""If the the answer is 'YES', provide the section name.
    Only return valid section names which are {section_names_text}.
    If the answer is 'NO' or 'NOT APPLICABLE', then output nothing.
    Provide a step by step justification for the answer.
    Format your response as a JSON object with 'answer', 'section name', and 'justification' as the keys.
    If the information isn't present, use 'unknown' as the value."""
    # -------------------------------------------------------------------------------------------


    prompt_instruction_A3_acl = f"""If the the answer is 'YES', provide the section name.
    Only return valid section names which are '{combined_node_id}'.
    If the answer is 'NO' or 'NOT APPLICABLE', then output nothing.
    Provide a step by step justification for the answer.
    Format your response as a JSON object with 'answer', 'section name', and 'justification' as the keys.
    If the information isn't present, use 'unknown' as the value."""

    if prompt_dict_choice == "acl":
        prompt_dict = generate_prompt_dict_acl(prompt_instruction_acl, prompt_instruction_A3_acl, combined_node_id)
    elif prompt_dict_choice == "neurips":
        prompt_dict = generate_prompt_dict_neurips(prompt_instruction_acl, combined_node_id)
    elif prompt_dict_choice == "neurips_b":
        prompt_dict = generate_prompt_dict_neurips_b(prompt_instruction_acl)
        


    # https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
    #embed_model = TogetherEmbedding(model_name="togethercomputer/m2-bert-80M-32k-retrieval", api_key = togetherai_api_key)
    embed_model = OpenAIEmbedding(model = 'text-embedding-ada-002')

    model_name = "gpt-4o-2024-05-13"
    llm = OpenAI(api_key=openai_api_key, temperature=0, model=model_name )

    #model_name = 'Llama-3-70b-chat-hf'

    #model_source = 'meta-llama'
    #model_name = f'{model_source}/Meta-Llama-3.1-70B-Instruct-Turbo'
    #llm = OpenAI(api_key=togetherai_api_key, temperature=0, model = model_name,base_url='https://api.together.xyz')

    """# Chunk References: Smaller Child Chunks Referring to Bigger Parent Chunk

    In this usage example, we show how to build a graph of smaller chunks pointing to bigger parent chunks.

    During query-time, we retrieve smaller chunks, but we follow references to bigger chunks. This allows us to have more context for synthesis.
    """

    # If the backend comes across issues that the author might like to know about
    # these issues will be provided to the author (e.g., papers missing limitations section get desk rejected)
    issue_dict_acl = {'A1': (A1_issue, 'Paper does not have a limitations section which according to https://aclrollingreview.org/cfp means the paper will get desk rejected.'),
                        'A2': (0, ''),
                        'A3': (0, ''),
                        'B1': (0, ''),
                        'B2': (0, ''),
                        'B3': (0, ''),
                        'B4': (0, ''),
                        'B5': (0, ''),
                        'B6': (0, ''),
                        'C1': (0, ''),
                        'C2': (0, ''),
                        'C3': (0, ''),
                        'C4': (0, ''),
                        'D1': (0, ''),
                        'D2': (0, ''),
                        'D3': (0, ''),
                        'D4': (0, ''),
                        'D5': (0, ''),
                        'E1': (0, '')
                        }

    sub_node_parsers = [SemanticSplitterNodeParser(buffer_size=1,
                                                breakpoint_percentile_threshold=95,
                                                embed_model=embed_model,
                                                include_metadata = True,
                                                include_prev_next_rel = True),]
    all_nodes = []
    send_update("Performing Embeddings")

    for base_node in base_nodes:
        for n in sub_node_parsers:
            sub_nodes = n.get_nodes_from_documents([base_node])
            sub_inodes = [
                IndexNode.from_text_node(sn, base_node.node_id) for sn in sub_nodes
            ]
            all_nodes.extend(sub_inodes)

        # also add original node to node
        original_node = IndexNode.from_text_node(base_node, base_node.node_id)
        all_nodes.append(original_node)

    all_nodes_dict = {n.node_id: n for n in all_nodes}

    index = VectorStoreIndex(all_nodes, embed_model=embed_model)


    # A1: Criterion for filtering nodes
    def is_limitation_node(node):
        return 'Limitation' in node.node_id

    # Filter the nodes based on the criterion
    A1_filtered_nodes = {node_id: node for node_id, node in all_nodes_dict.items() if is_limitation_node(node)}
    vector_retriever_chunk = index.as_retriever(similarity_top_k=40)

    recursive_retriever = RecursiveRetriever(
        "vector",
        retriever_dict={"vector": vector_retriever_chunk},
        node_dict=all_nodes_dict,
        verbose=False,
    )

    # https://docs.llamaindex.ai/en/v0.10.17/module_guides/deploying/query_engine/response_modes.html
    response_synthesizer = get_response_synthesizer(response_mode="tree_summarize")

    query_engine = RetrieverQueryEngine.from_args(
        recursive_retriever,
        response_synthesizer=response_synthesizer,
        llm=llm,
    )

    """## Outputting JSON Response."""

    results = {}
    valid_section_set = set(section_names)

    send_update("Running inference")
    for index ,key in enumerate(prompt_dict.keys()):
        send_update(f"Running Inference for Section {key[0]}")
        response = query_engine.query(prompt_dict[key])
        temp_dict = json.loads(response.response.replace('\\', '\\\\'))
        temp_dict['prompt'] = prompt_dict[key]
        temp_dict['llm'] = model_name
        
        # HALLUCINATION CHECK FOR ACL SECTION NAME RESPONSES  ----------------------------------
        if prompt_dict_choice == "acl" and "section" in temp_dict:
            returned_section = temp_dict.get("section", "").strip()
            if returned_section not in valid_section_set and returned_section.lower() != "none":
                temp_dict["hallucination_issue"] = (
                    f"Invalid section name: '{returned_section}' is not in the actual section list."
                )
                temp_dict["section"] = "None"
        # ----------------------------------------------------------------------------------------
        if "hallucination_issue" in temp_dict:
            print(f"Skipping hallucinated response for {key}: {temp_dict['hallucination_issue']}")
            continue
        results[key] = temp_dict

    results['issues'] = issue_dict_acl
    send_update("Inferencing Complete")

    return results