from collections import OrderedDict

# Supporting information https://neurips.cc/public/guides/PaperChecklist
supporting_prompt_dict = OrderedDict()

supporting_prompt_dict["1a"] = """The main claims made in the abstract and introduction should accurately reflect the paper's contributions and scope.
Claims should match theoretical and experimental results in terms of generalizability.
The paper's contributions should be clearly stated, along with important assumptions and limitations.
Aspirational goals can be used as motivation if it is clear they are not attained by the paper."""

supporting_prompt_dict["2a"] = """You are encouraged to create a separate "Limitations" section in your paper.
The paper should point out strong assumptions and how robust the results are to violations of these assumptions.
Reflect on how assumptions might be violated in practice and the implications.
Reflect on the scope of your claims, e.g., testing on a few datasets or limited runs.
Reflect on factors that influence performance, such as environmental conditions, resolution, or use in unintended contexts."""

supporting_prompt_dict["3a"] = """If including theoretical results, state all assumptions clearly in the theorem statements.
Include complete proofs either in the main paper or supplemental material, and provide a proof sketch for intuition if proofs are in the appendix.
All theorems and lemmas that the proof relies upon should be properly referenced."""

supporting_prompt_dict["4a"] = """If the contribution is a dataset or model, describe the steps taken to ensure reproducibility.
This may include releasing code and data, providing detailed instructions to replicate results, access to a model, or other means suitable for the research.
For closed-source models, ensure that other researchers have some path to reproduce or verify the results."""

supporting_prompt_dict["5a"] = """If you ran experiments, include the code, data, and instructions needed to reproduce the main experimental results.
Details such as the exact command and environment needed should be specified.
While release of code and data is encouraged, 'no' is acceptable if, for example, code is proprietary.
Remember to anonymize your release at submission time."""

supporting_prompt_dict["6a"] = """For experiments, specify all the training details, such as data splits, hyperparameters, and how they were chosen.
Details should be provided either in the main body or the supplemental materials.
The experimental setup should be presented with enough detail to appreciate and validate the results."""

supporting_prompt_dict["7a"] = """Report error bars or provide statistical significance of the experimental results.
Specify factors of variability that the error bars are capturing (e.g., random initialization, train/test split).
Provide details on how error bars were calculated (e.g., library call, bootstrap).
The type of error bar, such as standard deviation or standard error, should also be clarified."""

supporting_prompt_dict["8a"] = """For each experiment, provide sufficient information on computer resources used, such as type of compute workers (CPU/GPU), memory, time of execution.
Estimate the compute required for each run and disclose the total compute for the project, including preliminary or failed experiments."""

supporting_prompt_dict["9a"] = """Have you read the NeurIPS Code of Ethics and ensured your research conforms to it?
If special circumstances require deviation from the Code of Ethics, explain while preserving anonymity."""

supporting_prompt_dict["10a"] = """If applicable, discuss any potential negative societal impacts of your work.
Examples include malicious or unintended uses (e.g., surveillance, disinformation), fairness considerations, privacy concerns, and security risks.
Consider mitigation strategies, such as gated release of models or monitoring misuse."""

supporting_prompt_dict["11a"] = """If releasing models with high misuse potential, implement safeguards for responsible release.
Safeguards can include controlled access, requiring adherence to usage guidelines, or restrictions.
Describe how unsafe or offensive content in datasets has been managed to ensure safe release."""

supporting_prompt_dict["12a"] = """If using existing assets, cite creators and respect licenses.
State the version of the asset, license information, and any terms of use.
If releasing assets, include copyright information, terms of use, and a license."""

supporting_prompt_dict["13a"] = """If releasing new assets, document them thoroughly using structured templates.
Provide details such as training, license, and limitations.
Discuss whether and how consent was obtained from people whose data is used."""

supporting_prompt_dict["14a"] = """If you used crowdsourcing or conducted research with human subjects, include the full text of instructions given to participants and screenshots, if applicable.
Details about participant compensation should also be provided.
Ensure workers are paid at least the minimum wage in your country."""

supporting_prompt_dict["15a"] = """Did you describe potential participant risks and obtain IRB approval, if applicable?
State clearly whether IRB approval was obtained while preserving anonymity.
Adhere to NeurIPS Code of Ethics and the guidelines from your institution."""

def generate_prompt_dict_neurips_b(prompt_instruction):
    prompt_dict = OrderedDict()

    # 1a: Claims
    prompt_dict["1a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Do the main claims made in the abstract and introduction accurately reflect the paper's contributions and scope?
    Additional Context: {supporting_prompt_dict["1a"]}
    Output Structure: """ + prompt_instruction

    # 2a: Limitations
    prompt_dict["2a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you describe the limitations of your work?
    Additional Context: {supporting_prompt_dict["2a"]}
    Output Structure: """ + prompt_instruction

    # 3a: Theory, Assumptions and Proofs
    prompt_dict["3a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If you are including theoretical results, did you state the full set of assumptions and include complete proofs of all theoretical results?
    Additional Context: {supporting_prompt_dict["3a"]}
    Output Structure: """ + prompt_instruction

    # 4a: Experimental Result Reproducibility
    prompt_dict["4a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If the contribution is a dataset or model, what steps did you take to make your results reproducible or verifiable?
    Additional Context: {supporting_prompt_dict["4a"]}
    Output Structure: """ + prompt_instruction

    # 5a: Open Access to Data and Code
    prompt_dict["5a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If you ran experiments, did you include the code, data, and instructions needed to reproduce the main experimental results?
    Additional Context: {supporting_prompt_dict["5a"]}
    Output Structure: """ + prompt_instruction

    # 6a: Experimental Setting/ Details
    prompt_dict["6a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If you ran experiments, did you specify all the training details, including data splits, hyperparameters, and how they were chosen?
    Additional Context: {supporting_prompt_dict["6a"]}
    Output Structure: """ + prompt_instruction

    # 7a: Experiment Statistical Significance
    prompt_dict["7a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Does the paper report error bars suitably and correctly defined, or other appropriate information about the statistical significance of the experiments?
    Additional Context: {supporting_prompt_dict["7a"]}
    Output Structure: """ + prompt_instruction

    # 8a: Experiments Compute Resource
    prompt_dict["8a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: For each experiment, does the paper provide sufficient information on the computer resources used?
    Additional Context: {supporting_prompt_dict["8a"]}
    Output Structure: """ + prompt_instruction

    # 9a: Code of Ethics
    prompt_dict["9a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Have you read the NeurIPS Code of Ethics and ensured that your research conforms to it?
    Additional Context: {supporting_prompt_dict["9a"]}
    Output Structure: """ + prompt_instruction

    # 10a: Broader Impacts
    prompt_dict["10a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If appropriate, did you discuss potential negative societal impacts of your work?
    Additional Context: {supporting_prompt_dict["10a"]}
    Output Structure: """ + prompt_instruction

    # 11a: Safeguards
    prompt_dict["11a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Do you have safeguards in place for responsible release of models with a high risk for misuse?
    Additional Context: {supporting_prompt_dict["11a"]}
    Output Structure: """ + prompt_instruction

    # 12a: Licenses
    prompt_dict["12a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If you are using existing assets, did you cite the creators and respect the license and terms of use?
    Additional Context: {supporting_prompt_dict["12a"]}
    Output Structure: """ + prompt_instruction

    # 13a: Assets
    prompt_dict["13a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If you are releasing new assets, did you document them and provide these details alongside the assets?
    Additional Context: {supporting_prompt_dict["13a"]}
    Output Structure: """ + prompt_instruction

    # 14a: Crowdsourcing and Research with Human Subjects
    prompt_dict["14a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: If you used crowdsourcing or conducted research with human subjects, did you include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation?
    Additional Context: {supporting_prompt_dict["14a"]}
    Output Structure: """ + prompt_instruction

    # 15a: IRB Approvals
    prompt_dict["15a"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to NeurIPS.
    Question: Did you describe any potential participant risks and obtain Institutional Review Board (IRB) approvals, if applicable?
    Additional Context: {supporting_prompt_dict["15a"]}
    Output Structure: """ + prompt_instruction

    return prompt_dict

__all__ = ['generate_prompt_dict_neurips_b']