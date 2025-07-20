""" Script to compute stats about papers that are not on arXiv, or have blank checklists, no checklists, no section names, or all yes responses."""

import os
import re
import pandas as pd

def compute_acl_stats(subset):
    total_papers = len(subset)
    no_checklist = subset[subset['have_checklist'] == "No"]["paper"].tolist()
    question_cols = [col for col in subset.columns if col.startswith("acl_question_")]

    # --- BLANK CHECKLIST ---
    def is_blank_cell(val):
        """
        A cell is considered blank if its trimmed, lowercased value equals one of:
        "", "left blank", "no response", or "not applicable".
        """
        if pd.isna(val):
            return True
        s = str(val).strip().lower().rstrip('.')
        return s in {"", "left blank", "no response", "not applicable"}
    
    # --- NO SECTION NAMES ---
    def is_no_section_name_cell(val):
        """
        A cell qualifies as having NO section name if:
         - If the cell equals "not applicable", it's accepted.
         - Otherwise, if the cell starts with "[Yes]" or "[No]", remove the marker and any filler
           phrases ("left blank", "no response", "not applicable"). If nothing remains after that,
           then the cell is considered to have no section name.
        """
        if pd.isna(val):
            return False
        s = str(val).strip()
        s_lower = s.lower().rstrip('.')
        if s_lower == "not applicable":
            return True
        m = re.match(r'^\s*\[(yes|no)\]\s*(.*)$', s, re.IGNORECASE)
        if not m:
            return False
        remainder = m.group(2).strip()
        # Remove filler phrases (case-insensitive)
        remainder_clean = re.sub(r'(?i)\b(left blank|no response|not applicable)\b', '', remainder).strip()
        # Remove trailing punctuation if any
        remainder_clean = remainder_clean.rstrip('.').strip()
        return remainder_clean == ""
    
    def row_is_no_section_names(row):
        """
        A row qualifies as "no section names" if:
         - It is not entirely blank (i.e. at least one cell is non-blank), AND
         - Every non-blank cell qualifies as having no section name.
        """
        non_blank = [val for val in row if not is_blank_cell(val)]
        if not non_blank:
            return False
        return all(is_no_section_name_cell(val) for val in non_blank)
    
    # --- ALL YES RESPONSES ---
    def is_all_yes_cell(val):
        """
        A cell qualifies as a positive ("yes") answer if:
         - It starts with "[Yes]" (even if extra details follow), or
         - It equals (or contains) "not applicable",
        and if it does not contain "[No]".
        """
        if pd.isna(val):
            return False
        s = str(val).strip().lower().rstrip('.')
        if "[no]" in s:
            return False
        return s.startswith("[yes]") or s == "not applicable" or "not applicable" in s
    
    def row_is_all_yes(row):
        """
        A row qualifies as "all yes" if every non-blank cell qualifies as a yes cell.
        """
        non_blank = [val for val in row if not is_blank_cell(val)]
        if not non_blank:
            return False
        return all(is_all_yes_cell(val) for val in non_blank)
    
    # --- Filter rows ---
    blank_checklist = subset[
        (subset['have_checklist'] == "Yes") &
        (subset[question_cols].fillna("").apply(lambda row: all(is_blank_cell(val) for val in row), axis=1))
    ]["paper"].tolist()
    
    no_section_names = subset[
        subset[question_cols].fillna("").apply(lambda row: row_is_no_section_names(row), axis=1)
    ]["paper"].tolist()
    
    all_yes_responses = subset[
        subset[question_cols].fillna("").apply(lambda row: row_is_all_yes(row), axis=1)
    ]["paper"].tolist()
    
    not_on_arxiv = subset[
        subset['arxiv_link'].isna() | (subset['arxiv_link'].str.strip() == "")
    ]["paper"].tolist()
    
    def save_paper_list(category_name, paper_list):
        directory = "/Users/vidhyakshayakannan/EvaluationConfReady/edge cases/acl edge cases"
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, f"{category_name}_papers.txt")
        with open(filename, "w") as f:
            for paper in paper_list:
                f.write(f"{paper}\n")
        print(f"\nSaved {len(paper_list)} papers to {filename}\n")
    
    save_paper_list("no_checklist", no_checklist)
    save_paper_list("blank_checklist", blank_checklist)
    save_paper_list("no_section_names", no_section_names)
    save_paper_list("all_yes_responses", all_yes_responses)
    save_paper_list("not_on_arxiv", not_on_arxiv)
    
    return [
        total_papers,
        len(no_checklist),
        len(blank_checklist),
        len(no_section_names),
        len(all_yes_responses),
        len(not_on_arxiv)
    ]

def compute_neurips_stats(subset):
    total_papers = len(subset)
    question_cols = [col for col in subset.columns if col.startswith("neurips_") and not col.endswith("_llm")]

    def is_blank_cell(val):
        if pd.isna(val):
            return True
        val_str = str(val).strip().lower()
        return val_str in ["", "no response", "left blank", "not applicable", "[na]", "[]"]

    def normalized_answer(val):
        if pd.isna(val):
            return ""
        s = str(val).strip().lower()
        for phrase in ["left blank", "no response", "not applicable", "[na]", "[]"]:
            s = s.replace(phrase, "").strip()
        return s

    no_checklist_papers = subset[subset['have_checklist'] == "No"]['paper'].tolist()
    blank_checklist_papers = subset[
        (subset['have_checklist'] == "Yes") &
        (subset[question_cols].fillna("").apply(lambda row: all(is_blank_cell(val) for val in row), axis=1))
    ]['paper'].tolist()
    all_yes_papers = subset[
        subset[question_cols].fillna("").apply(
            lambda row: all("[yes]" in str(val).lower() for val in row),
            axis=1
        )
    ]['paper'].tolist()
    no_section_name_papers = subset[
        subset[question_cols].fillna("").apply(
            lambda row: all(normalized_answer(val) in ["[yes]", "[no]", ""] for val in row),
            axis=1
        )
    ]['paper'].tolist()
    not_on_arxiv_papers = subset[
        subset['arxiv_link'].isna() | (subset['arxiv_link'].str.strip() == "")
    ]['paper'].tolist()

    def save_paper_list(category_name, paper_list):
        base_path = "/Users/vidhyakshayakannan/EvaluationConfReady/edge cases/neurips edge cases/"
        os.makedirs(base_path, exist_ok=True)
        filename = f"{category_name}_papers.txt"
        full_path = os.path.join(base_path, filename)
        with open(full_path, "w") as f:
            for paper in paper_list:
                f.write(f"{paper}\n")
        print(f"\nSaved {len(paper_list)} papers to {full_path}\n")

    save_paper_list("no_checklist", no_checklist_papers)
    save_paper_list("blank_checklist", blank_checklist_papers)
    save_paper_list("all_yes_responses", all_yes_papers)
    save_paper_list("no_section_names", no_section_name_papers)
    save_paper_list("not_on_arxiv", not_on_arxiv_papers)

    return [
        total_papers, 
        len(no_checklist_papers), 
        len(blank_checklist_papers), 
        len(all_yes_papers), 
        len(no_section_name_papers), 
        len(not_on_arxiv_papers)
    ]

def compute_neurips_db(subset):
    total_papers = len(subset)
    question_cols = [col for col in subset.columns if col.startswith("neurips_question_") and not col.endswith("_llm")]

    def is_blank_cell(val):
        if pd.isna(val):
            return True
        val_str = str(val).strip().lower()
        return val_str in ["", "[na]", "[]"]

    def normalized_answer(val):
        if pd.isna(val):
            return ""
        s = str(val).strip().lower()
        for phrase in ["[na]", "[]"]:
            s = s.replace(phrase, "").strip()
        return s

    no_checklist_papers = subset[subset['have_checklist'] == "No"]['paper'].tolist()
    blank_checklist_papers = subset[
        (subset['have_checklist'] == "Yes") &
        (subset[question_cols].fillna("").apply(lambda row: all(is_blank_cell(val) for val in row), axis=1))
    ]['paper'].tolist()

    all_yes_papers = subset[
        subset[question_cols].fillna("").apply(
            lambda row: all(str(val).strip().lower() in ["[yes]", "[n/a]", ["na"]] for val in row),
            axis=1
        )
    ]['paper'].tolist()

    no_section_name_papers = subset[
        subset[question_cols].fillna("").apply(
            lambda row: all(normalized_answer(val) in ["[yes]", "[no]", ""] for val in row),
            axis=1
        )
    ]['paper'].tolist()

    not_on_arxiv_papers = subset[
        subset['arxiv_link'].isna() | (subset['arxiv_link'].str.strip() == "")
    ]['paper'].tolist()

    def save_paper_list(category_name, paper_list):
        base_path = "/Users/vidhyakshayakannan/EvaluationConfReady/edge cases/neurips db edge cases"
        os.makedirs(base_path, exist_ok=True)
        filename = f"{category_name}_papers.txt"
        full_path = os.path.join(base_path, filename)
        with open(full_path, "w") as f:
            for paper in paper_list:
                f.write(f"{paper}\n")
        print(f"\nSaved {len(paper_list)} papers to {full_path}\n")

    save_paper_list("no_checklist", no_checklist_papers)
    save_paper_list("blank_checklist", blank_checklist_papers)
    save_paper_list("all_yes_responses", all_yes_papers)
    save_paper_list("no_section_names", no_section_name_papers)
    save_paper_list("not_on_arxiv", not_on_arxiv_papers)

    return [
        total_papers, 
        len(no_checklist_papers), 
        len(blank_checklist_papers), 
        len(all_yes_papers), 
        len(no_section_name_papers), 
        len(not_on_arxiv_papers)
    ]

# -------------------------------
# ACL Findings
# -------------------------------
file_path_findings = "/Users/vidhyakshayakannan/EvaluationConfReady/final datasets/acl/updated_findings_long_short.xlsx"
df_findings = pd.read_excel(file_path_findings, engine="openpyxl", sheet_name=0)
df_findings['long/short'] = ['long' if idx <= 713 else 'short' for idx in df_findings.index]

acl_findings_long = df_findings[df_findings['long/short'].str.lower() == "long"]
acl_findings_short = df_findings[df_findings['long/short'].str.lower() == "short"]


acl_findings_short_stats = compute_acl_stats(acl_findings_short)
acl_findings_long_stats = compute_acl_stats(acl_findings_long)

# -------------------------------
# ACL Main
# -------------------------------
file_path_main = "/Users/vidhyakshayakannan/EvaluationConfReady/final datasets/acl/updated_main_long_short.xlsx"
df_main = pd.read_excel(file_path_main)
df_main['long/short'] = df_main['acl_link'].apply(
    lambda x: 'long' if 'long' in str(x).lower() else ('short' if 'short' in str(x).lower() else '')
)

acl_main_long = df_main[df_main['long/short'] == "long"]
acl_main_short = df_main[df_main['long/short'] == "short"]

acl_main_short_stats = compute_acl_stats(acl_main_short)
acl_main_long_stats = compute_acl_stats(acl_main_long)

# -------------------------------
# NeurIPS Main
# -------------------------------
file_path_neurips = "/Users/vidhyakshayakannan/EvaluationConfReady/final datasets/neurips/neurips_main_24_dataset.xlsx"
df_neurips = pd.read_excel(file_path_neurips)
neurips_stats = compute_neurips_stats(df_neurips)

# -------------------------------
# NeurIPS D&B
# -------------------------------
file_path_neurips_db = "/Users/vidhyakshayakannan/EvaluationConfReady/final datasets/neurips_db/neurips_db_24_accept.xlsx"
df_neurips_db = pd.read_excel(file_path_neurips_db)
neurips_db_stats = compute_neurips_db(df_neurips_db)

table = pd.DataFrame({
    "ACL Findings Short": acl_findings_short_stats,
    "ACL Findings Long":  acl_findings_long_stats,
    "ACL Main Short":     acl_main_short_stats,
    "ACL Main Long":      acl_main_long_stats,
    "NeurIPS Main":       neurips_stats,
    "NeurIPS D&B":        neurips_db_stats
}, index=[
    "Total Papers",
    "No Checklist",
    "Blank Checklist",
    "All Yes Responses",
    "No Section Names",
    "Not on arXiv"
])

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(table)
