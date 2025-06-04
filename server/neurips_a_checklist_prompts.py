from collections import OrderedDict

# Supporting information from NeurIPS Paper Checklist
supporting_prompt_dict = OrderedDict()

supporting_prompt_dict["1"] = """Use the content of the abstract and introduction. 
Ensure that the claims align with the paper’s contributions and scope."""

supporting_prompt_dict["2"] = """Look for a discussion of limitations, often in a 'Limitations' or 'Discussion' section. 
Ensure assumptions and scope are reflected."""

supporting_prompt_dict["3"] = """Only applicable if theoretical results exist. 
Verify that full assumptions and complete proofs are provided in the main text or supplemental."""

supporting_prompt_dict["4"] = """If the paper includes experiments, verify that all information needed to reproduce them is disclosed, regardless of code availability."""

supporting_prompt_dict["5"] = """Check if data and code are provided with sufficient instructions for faithful reproduction, or justify why not."""

supporting_prompt_dict["6"] = """Verify that training and test details (e.g., data splits, hyperparameters, optimizer) are specified."""

supporting_prompt_dict["7"] = """If experiments exist, check for statistical significance measures (error bars, confidence intervals) and explanation of how they were calculated."""

supporting_prompt_dict["8"] = """Check that compute resources (type of hardware, memory, execution time) are described for each experiment."""

supporting_prompt_dict["9"] = """Ensure the research conforms to the NeurIPS Code of Ethics by checking for any harmful consequences or deviations."""

supporting_prompt_dict["10"] = """Verify discussion of both positive and negative societal impacts of the work, or justify if none."""

supporting_prompt_dict["11"] = """Check for safeguards in place when releasing high-risk data or models (e.g., usage guidelines, filters)."""

supporting_prompt_dict["12"] = """Verify that existing assets are properly credited, including license and terms of use of datasets, code, or models."""

supporting_prompt_dict["13"] = """If new assets are introduced, ensure they are well documented and that consent procedures (if applicable) are described."""

supporting_prompt_dict["14"] = """If crowdsourcing or human subjects are involved, check for full instructions to participants, screenshots, and compensation details."""

supporting_prompt_dict["15"] = """Verify that IRB approval (or equivalent) and participant risk descriptions are provided for any human subjects research."""

def generate_prompt_dict_neurips_a():
    prompt_dict = OrderedDict()
    prompt_instruction = "Return your answer as a JSON object with keys: 'answer', 'section name', and 'justification'. 'answer' should be one of 'Yes', 'No', or 'N/A'."
    
    # 1: Claims
    prompt_dict["1"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?
    Additional Context: {supporting_prompt_dict["1"]}
    Output Structure: """ + prompt_instruction
    
    # 2: Limitations
    prompt_dict["2"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper discuss the limitations of the work performed by the authors?
    Additional Context: {supporting_prompt_dict["2"]}
    Output Structure: """ + prompt_instruction
        
    # 3: Theory Assumptions and Proofs
    prompt_dict["3"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof?
    Additional Context: {supporting_prompt_dict["3"]}
    Output Structure: """ + prompt_instruction
        
    # 4: Experimental Result Reproducibility
    prompt_dict["4"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)?
    Additional Context: {supporting_prompt_dict["4"]}
    Output Structure: """ + prompt_instruction
    
    # 5: Open access to data and code
    prompt_dict["5"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material?
    Additional Context: {supporting_prompt_dict["5"]}
    Output Structure: """ + prompt_instruction
    
    # 6: Experimental Setting/Details
    prompt_dict["6"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results?
    Additional Context: {supporting_prompt_dict["6"]}
    Output Structure: """ + prompt_instruction
    
    # 7: Experiment Statistical Significance
    prompt_dict["7"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments?
    Additional Context: {supporting_prompt_dict["7"]}
    Output Structure: """ + prompt_instruction
    
    # 8: Experiments Compute Resources
    prompt_dict["8"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments?
    Additional Context: {supporting_prompt_dict["8"]}
    Output Structure: """ + prompt_instruction
    
    # 9: Code Of Ethics
    prompt_dict["9"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics (https://neurips.cc/public/EthicsGuidelines)?
    Additional Context: {supporting_prompt_dict["9"]}
    Output Structure: """ + prompt_instruction
        
    # 10: Broader Impacts
    prompt_dict["10"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed?
    Additional Context: {supporting_prompt_dict["10"]}
    Output Structure: """ + prompt_instruction
    
    # 11: Safeguards
    prompt_dict["11"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)?
    Additional Context: {supporting_prompt_dict["11"]}
    Output Structure: """ + prompt_instruction
    
    # 12: Licenses for existing assets
    prompt_dict["12"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected?
    Additional Context: {supporting_prompt_dict["12"]}
    Output Structure: """ + prompt_instruction
        
    # 13: New Assets
    prompt_dict["13"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets?
    Additional Context: {supporting_prompt_dict["13"]}
    Output Structure: """ + prompt_instruction
    
    # 14: Crowdsourcing and Research with Human Subjects
    prompt_dict["14"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)?
    Additional Context: {supporting_prompt_dict["14"]}
    Output Structure: """ + prompt_instruction
    
    # 15: Institutional Review Board (IRB) Approvals or Equivalent
    prompt_dict["15"] = f"""Introduction: Behave like you are the author of a NeurIPS paper.
    Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained?
    Additional Context: {supporting_prompt_dict["15"]}
    Output Structure: """ + prompt_instruction
    
    return prompt_dict

generate_prompt_dict_neurips = generate_prompt_dict_neurips_a
__all__ = ['generate_prompt_dict_neurips_a', 'generate_prompt_dict_neurips']