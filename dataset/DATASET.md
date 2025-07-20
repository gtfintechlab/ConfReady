# ACL Dataset Overview

This dataset contains checklist evaluations for papers from the **ACL 2023 conference**, split into long and short paper categories. It contains both the **authors’ original responses** to the reproducibility checklist and **LLM-generated responses** for those questions.

---

## 1. `ACL Main Long`

- **Papers**: 910  
- **Description**: Long-form papers submitted to ACL 2023, with responses to 22 reproducibility-related questions.
- **Structure**:
  - `paper`, `acl_link`, `arxiv_link`: Metadata.
  - `have_checklist`: Indicates whether authors completed the checklist.
  - `acl_question_*`: Author responses to questions `a1`–`d5`.
  - `acl_question_*_llm`: LLM-based inferences on each response (can be blank if not available).

---

## `ACL Main Short`

- **Papers**: 164  
- **Description**: Short papers from ACL 2023 with the same structure as the long papers.
- **Note**: Some papers do not include a checklist (`have_checklist = No`).

---
## `ACL Findings Short`

- **Papers**: 189
- **Description**: Short papers published in the **Findings of ACL** track. 
- **Structure**: Same columns as `ACL Main Long` and `Short`.
--
## `ACL Findings Long`

- **Papers**: 712
- **Description**: Long papers published in the **Findings of ACL** track. 
- **Structure**: Same columns as `ACL Main Long` and `Short`.


## Checklist Question Format

Each question belongs to a category:

### A. Limitations and Ethics
- `a1`: Limitations discussed?
- `a2`: Broader impacts described?
- `a3`: Ethical considerations disclosed?
- `a4`: Potential negative impacts identified?

### B. Data
- `b1`: Dataset source described?
- `b2`: Licensing included?
- `b3`: Dataset accessible?
- `b4`: Documentation provided?
- `b5`: Data anonymization addressed?
- `b6`: Any data curation mentioned?

### C. Code and Evaluation
- `c1`: Code publicly released?
- `c2`: Evaluation setup described?
- `c3`: Results clearly reported?
- `c4`: Compute/resources disclosed?

### D. Human Evaluation
- `d1`: Instructions for evaluators shared?
- `d2`: Evaluator demographics described?
- `d3`: Evaluation methodology detailed?
- `d4`: Human review biases discussed?
- `d5`: Crowdwork platform and compensation explained?

Each question has two fields:
- `acl_question_X`: Raw author answer  
- `acl_question_X_llm`: LLM-generated interpretation 

---

## Example Columns

| Column                | Description                                  |
|-----------------------|----------------------------------------------|
| `acl_question_a1`     | Did the authors discuss the limitations?     |
| `acl_question_a1_llm` | LLM’s Yes/No judgment on that response       |
| `acl_question_b3`     | Is the dataset publicly available?           |
| `acl_question_d2`     | Was human evaluation clearly described?      |

---

## 🕵️‍♀️ Edge‑Case Summary

The script flags five notorious edge cases:

1. **No Checklist** – `have_checklist = "No"`.
2. **Blank Checklist** – authors marked “Yes” but left every answer blank.
3. **All Yes Responses** – every non‑blank cell starts with `[Yes]` (or *Not applicable*).
4. **No Section Names** – answers say `[Yes]`/`[No]` but don’t cite any paper section.
5. **Not on arXiv** – `arxiv_link` missing or empty.

|                   | ACL Fnd Short | ACL Fnd Long | ACL Main Short | ACL Main Long 
|:------------------|-------------:|------------:|--------------:|-------------:|-------------:|------------:|
| **Total Papers**      | 189 | 712 | 164 | 910 | 
| **No Checklist**      | 8 | 19 | 3 | 15 |
| **Blank Checklist**   | 8 | 35 | 10 | 60 |
| **All Yes Responses** | 7 | 15 | 3 | 28 | 
| **No Section Names**  | 5 | 7 | 2 | 9 | 
| **Not on arXiv**      | 50 | 190 | 37 | 190 | 

> **Why it matters:** spotting these patterns helps triage papers that need manual follow‑up. 
---


## Use Cases

- Compare **human-written vs LLM-inferred** checklist responses

- Evaluate models on **checklist responses**

---
