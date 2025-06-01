from collections import OrderedDict

# Supporting information https://neurips.cc/public/guides/PaperChecklist
supporting_prompt_dict = OrderedDict()

# section 1 =========================================================================================================

supporting_prompt_dict["1a"] = """The main claims made in the abstract and introduction should accurately reflect the paper's contributions and scope.
Claims should match theoretical and experimental results in terms of generalizability.
The paper's contributions should be clearly stated, along with important assumptions and limitations.
Aspirational goals can be used as motivation if it is clear they are not attained by the paper."""

supporting_prompt_dict["1b"] = """Look for a discussion of limitations, often found in a 'Limitations' or 'Discussion' section."""

supporting_prompt_dict["1c"] = """Refer to sections discussing ethical implications or societal impacts. 
If there are no negative societal impacts, justify why it is not applicable."""

supporting_prompt_dict["1d"] = """Check for statements about following NeurIPS ethics review guidelines. 
Look for explicit confirmation in the main text or appendices."""

#  ==================================================================================================================

# section 2 =========================================================================================================

supporting_prompt_dict["2a"] = """Only applicable if the paper includes theoretical results. 
Verify that all assumptions underlying those results are stated clearly.
The paper should point out strong assumptions and how robust the results are to violations of these assumptions.
Reflect on how assumptions might be violated in practice and the implications.
Reflect on the scope of your claims, e.g., testing on a few datasets or limited runs.
Reflect on factors that influence performance, such as environmental conditions, resolution, or use in unintended contexts."""

supporting_prompt_dict["2b"] = """Only applicable if the paper includes theoretical results. 
Verify that complete proofs are provided either in the main text or in the appendix."""

#  ==================================================================================================================

# section 3 =========================================================================================================

supporting_prompt_dict["3a"] = """Check for GitHub links, supplemental material, or URLs providing code, data, and instructions for reproducing experiments."""

supporting_prompt_dict["3b"] = """Look in the experimental details section for data splits, hyperparameters, and descriptions of how they were chosen."""

supporting_prompt_dict["3c"] = """Determine if results include mean and standard deviation or other error bars over multiple runs."""

supporting_prompt_dict["3d"] = """Look for mentions of compute resources (e.g., GPU types, cluster details, cloud provider) in the experimental setup."""

#  ==================================================================================================================

# section 4 =========================================================================================================

supporting_prompt_dict["4a"] = """Verify that all reused datasets, models, or code are cited properly in the references."""

supporting_prompt_dict["4b"] = """Check for statements about licenses (e.g., MIT, CC-BY) for any existing assets used."""

supporting_prompt_dict["4c"] = """Determine if any new datasets or tools are released, with links or supplemental files provided."""

supporting_prompt_dict["4d"] = """For datasets involving human data, verify that consent procedures are discussed (e.g., in methods or appendix)."""

supporting_prompt_dict["4e"] = """Check for statements about whether the used or curated data contain personally identifiable information or offensive content, often in an 'Ethics' section or appendix."""

#  ==================================================================================================================

# section 5 =========================================================================================================

supporting_prompt_dict["5a"] = """Look for the full text of instructions given to workers or screenshots of the annotation interface, if applicable."""

supporting_prompt_dict["5b"] = """Verify that any participant risks are discussed, with IRB approval details if necessary."""

supporting_prompt_dict["5c"] = """Check for statements about compensation, including hourly wage or total amount spent on participant compensation."""

#  ==================================================================================================================

def generate_prompt_dict_neurips_b():
    prompt_dict = OrderedDict()
    prompt_instruction = "Return your answer as a JSON object with keys: 'answer', 'section name', and 'justification'. 'answer' must be one of 'Yes', 'No', or 'N/A'."
    
    # 1a: Main claims in abstract/introduction
    prompt_dict["1a"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?
    Additional Context: {supporting_prompt_dict["1a"]}
    Output Structure: """ + prompt_instruction
    
    # 1b: Limitations
    prompt_dict["1b"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you describe the limitations of your work?
    Additional Context: {supporting_prompt_dict["1b"]}
    Output Structure: """ + prompt_instruction
    
    # 1c: Negative societal impacts
    prompt_dict["1c"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you discuss any potential negative societal impacts of your work?
    Additional Context: {supporting_prompt_dict["1c"]}
    Output Structure: """ + prompt_instruction
    
    # 1d: Ethics review guidelines
    prompt_dict["1d"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Have you read the ethics review guidelines and ensured that your paper conforms to them?
    Additional Context: {supporting_prompt_dict["1d"]}
    Output Structure: """ + prompt_instruction
    
    # 2a: Theoretical assumptions
    prompt_dict["2a"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you state the full set of assumptions of all theoretical results?
    Additional Context: {supporting_prompt_dict["2a"]}
    Output Structure: """ + prompt_instruction
    
    # 2b: Theoretical proofs
    prompt_dict["2b"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you include complete proofs of all theoretical results?
    Additional Context: {supporting_prompt_dict["2b"]}
    Output Structure: """ + prompt_instruction
    
    # 3a: Reproducibility (code/data)
    prompt_dict["3a"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)?
    Additional Context: {supporting_prompt_dict["3a"]}
    Output Structure: """ + prompt_instruction
    
    # 3b: Training details
    prompt_dict["3b"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you specify all the training details (e.g., data splits, hyperparameters, how they were chosen)?
    Additional Context: {supporting_prompt_dict["3b"]}
    Output Structure: """ + prompt_instruction
    
    # 3c: Error bars
    prompt_dict["3c"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you report error bars (e.g., with respect to the random seed after running experiments multiple times)?
    Additional Context: {supporting_prompt_dict["3c"]}
    Output Structure: """ + prompt_instruction
    
    # 3d: Compute resources
    prompt_dict["3d"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you include the total amount of compute and the type of resources used (e.g., type of GPUs, internal cluster, or cloud provider)?
    Additional Context: {supporting_prompt_dict["3d"]}
    Output Structure: """ + prompt_instruction
    
    # 4a: Cite creators of existing assets
    prompt_dict["4a"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: If your work uses existing assets, did you cite the creators?
    Additional Context: {supporting_prompt_dict["4a"]}
    Output Structure: """ + prompt_instruction
    
    # 4b: Mention license of assets
    prompt_dict["4b"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you mention the license of the assets?
    Additional Context: {supporting_prompt_dict["4b"]}
    Output Structure: """ + prompt_instruction
    
    # 4c: New assets included
    prompt_dict["4c"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you include any new assets either in the supplemental material or as a URL?
    Additional Context: {supporting_prompt_dict["4c"]}
    Output Structure: """ + prompt_instruction
    
    # 4d: Consent from data subjects
    prompt_dict["4d"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you discuss whether and how consent was obtained from people whose data you’re using/curating?
    Additional Context: {supporting_prompt_dict["4d"]}
    Output Structure: """ + prompt_instruction
    
    # 4e: PII or offensive content
    prompt_dict["4e"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you discuss whether the data you are using/curating contains personally identifiable information or offensive content?
    Additional Context: {supporting_prompt_dict["4e"]}
    Output Structure: """ + prompt_instruction
    
    # 5a: Full instructions to participants
    prompt_dict["5a"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you include the full text of instructions given to participants and screenshots, if applicable?
    Additional Context: {supporting_prompt_dict["5a"]}
    Output Structure: """ + prompt_instruction
    
    # 5b: Participant risks and IRB
    prompt_dict["5b"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you describe any potential participant risks, with links to Institutional Review Board (IRB) approvals, if applicable?
    Additional Context: {supporting_prompt_dict["5b"]}
    Output Structure: """ + prompt_instruction
    
    # 5c: Participant compensation details
    prompt_dict["5c"] = f"""Introduction: Behave like you are the author of a NeurIPS Datasets and Benchmarks submission.
    Question: Did you include the estimated hourly wage paid to participants and the total amount spent on participant compensation?
    Additional Context: {supporting_prompt_dict["5c"]}
    Output Structure: """ + prompt_instruction

    return prompt_dict

__all__ = ['generate_prompt_dict_neurips_b']