from collections import OrderedDict

# Supporting information from https://neurips.cc/Conferences/2021/PaperInformation/PaperChecklist
supporting_prompt_dict = OrderedDict()

supporting_prompt_dict["1a"] = """The main claims made in the abstract and introduction should accurately reflect the paper's contributions and scope.
Claims in the paper should match theoretical and experimental results in terms of how much the results can be expected to generalize.
The paper's contributions should be clearly stated in the abstract and introduction, along with any important assumptions and limitations. Aspirational goals can be used as motivation if they are clearly distinguished from the contributions."""

supporting_prompt_dict["1b"] = """You should read the ethics review guidelines provided by NeurIPS and ensure your paper conforms to these guidelines."""

supporting_prompt_dict["1c"] = """Examples of potential negative societal impacts include malicious or unintended uses (e.g., disinformation, surveillance), environmental impacts (e.g., training large models), fairness considerations (e.g., disadvantaging specific groups), privacy considerations, and security considerations.
Consider different stakeholders who might be affected by the work, especially marginalized communities. Discuss both intended positive uses and possible harms from misuse.
Mention mitigation strategies, such as gated release of models, monitoring misuse, or improving ML efficiency and accessibility."""

supporting_prompt_dict["1d"] = """Point out any strong assumptions and reflect on how robust your results are to violations of these assumptions. Explain how these assumptions could be violated in practice and what the implications would be.
You are encouraged to have a separate 'Limitations' section in your paper, and reviewers are instructed not to penalize honesty concerning limitations."""

supporting_prompt_dict["2a"] = """If your work includes theoretical results, all assumptions should be clearly stated in the theorem statements. This ensures transparency and reproducibility of the results."""

supporting_prompt_dict["2b"] = """If the paper contains theoretical results, proofs should be included either in the main body or the supplemental material. A proof sketch can be included in the main body to provide intuition, even if the full proof is in the appendix."""

supporting_prompt_dict["3a"] = """If your work includes experimental results, include the code, data, and instructions to reproduce the main experimental results. Anonymize code and data at submission time if necessary.
Try to include all minor experiments from the paper as well."""

supporting_prompt_dict["3b"] = """If you ran experiments, provide full training details, including data splits, hyperparameters, and how they were chosen.
Important details should be in the main body, while additional details can be included in the supplemental material."""

supporting_prompt_dict["3c"] = """Report error bars (e.g., from random seeds) or statistical significance tests for your main experiments. Include confidence intervals if applicable."""

supporting_prompt_dict["3d"] = """Include the compute used for each experimental run, including the type of resources used (e.g., GPUs, cloud provider). If available, use CO2 emissions trackers and provide that information."""

supporting_prompt_dict["4a"] = """If your work uses existing assets, cite the creators and specify the version of the asset used. Mention URLs if applicable."""

supporting_prompt_dict["4b"] = """Mention the license for the assets used (e.g., CC-BY 4.0). If you scraped data, mention copyright and terms of service. Include license information for assets released with your paper."""

supporting_prompt_dict["4c"] = """If you are including new assets, anonymize them at submission. If they cannot be released, explain why."""

supporting_prompt_dict["4d"] = """If you collected data, discuss whether consent was obtained. Even if the data came from an existing dataset, make an effort to understand how it was collected and if consent was obtained."""

supporting_prompt_dict["4e"] = """If the data used contains personally identifiable information or offensive content, explain how you checked for this (e.g., scripts, manual sampling). Discuss steps taken to anonymize the data."""

supporting_prompt_dict["5a"] = """If you collected data from human subjects, include the full instructions given to participants (screenshots, if applicable). Including these in supplemental material is acceptable if the main contribution doesn't involve human subjects."""

supporting_prompt_dict["5b"] = """Describe any potential risks to participants, with links to Institutional Review Board (IRB) approvals if applicable. State clearly whether IRB approval was obtained."""

supporting_prompt_dict["5c"] = """Include the estimated hourly wage paid to participants and the total amount spent on compensation. Discuss how you determined the wage and ensured that it was fair."""

def generate_prompt_dict_neurips(prompt_instruction, combined_node_id):
    prompt_dict = OrderedDict()

    # A: For All Authors
    prompt_dict["1a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Do the main claims made in the abstract and introduction accurately reflect the paper's contributions and scope?
    Additional Context: {supporting_prompt_dict["1a"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["1b"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Have you read the ethics review guidelines and ensured that your paper conforms to them?
    Additional Context: {supporting_prompt_dict["1b"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["1c"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you discuss any potential negative societal impacts of your work?
    Additional Context: {supporting_prompt_dict["1c"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["1d"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you describe the limitations of your work?
    Additional Context: {supporting_prompt_dict["1d"]}
    Output Structure: """ + prompt_instruction

    # B: If You Are Including Theoretical Results
    prompt_dict["2a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you state the full set of assumptions of all theoretical results?
    Additional Context: {supporting_prompt_dict["2a"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["2b"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you include complete proofs of all theoretical results?
    Additional Context: {supporting_prompt_dict["2b"]}
    Output Structure: """ + prompt_instruction

    # C: If You Ran Experiments
    prompt_dict["3a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you include the code, data, and instructions needed to reproduce the main experimental results?
    Additional Context: {supporting_prompt_dict["3a"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["3b"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you specify all the training details (e.g., data splits, hyperparameters, how they were chosen)?
    Additional Context: {supporting_prompt_dict["3b"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["3c"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you report error bars (e.g., with respect to the random seed after running experiments multiple times)?
    Additional Context: {supporting_prompt_dict["3c"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["3d"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you include the amount of compute and the type of resources used (e.g., type of GPUs, internal cluster, or cloud provider)?
    Additional Context: {supporting_prompt_dict["3d"]}
    Output Structure: """ + prompt_instruction

    # D: If You Are Using Existing Assets (e.g., Code, Data, Models)
    prompt_dict["4a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If your work uses existing assets, did you cite the creators?
    Additional Context: {supporting_prompt_dict["4a"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["4b"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you mention the license of the assets?
    Additional Context: {supporting_prompt_dict["4b"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["4c"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you include any new assets either in the supplemental material or as a URL?
    Additional Context: {supporting_prompt_dict["4c"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["4d"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you discuss whether and how consent was obtained from people whose data you're using/curating?
    Additional Context: {supporting_prompt_dict["4d"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["4e"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you discuss whether the data you are using/curating contains personally identifiable information or offensive content?
    Additional Context: {supporting_prompt_dict["4e"]}
    Output Structure: """ + prompt_instruction

    # E: If You Conducted Research With Human Subjects
    prompt_dict["5a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you include the full text of instructions given to participants and screenshots, if applicable?
    Additional Context: {supporting_prompt_dict["5a"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["5b"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you describe any potential participant risks, with links to Institutional Review Board (IRB) approvals, if applicable?
    Additional Context: {supporting_prompt_dict["5b"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["5c"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you include the estimated hourly wage paid to participants and the total amount spent on participant compensation?
    Additional Context: {supporting_prompt_dict["5c"]}
    Output Structure: """ + prompt_instruction

    return prompt_dict

# Export the function to generate prompt_dict
__all__ = ['generate_prompt_dict_neurips']

