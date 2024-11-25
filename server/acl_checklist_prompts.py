from collections import OrderedDict

    # Supporting information is taken from https://aclrollingreview.org/responsibleNLPresearch/
supporting_prompt_dict = OrderedDict()
supporting_prompt_dict["A1"] = """Point out any strong assumptions and how robust your results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only held locally). Reflect on how these assumptions might be violated in practice and what the implications would be.
    Reflect on the scope of your claims, e.g., if you only tested your approach on a few datasets, languages, or did a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated. Reflect on the factors that influence the performance of your approach. For example, a speech-to-text system might not be able to be reliably used to provide closed captions for online lectures because it fails to handle technical jargon.
    If you analyze model biases: state the definition of bias you are using. State the motivation and definition explicitly."""

supporting_prompt_dict["A2"] = """Examples of risks include potential malicious or unintended harmful effects and uses (e.g., disinformation, generating fake profiles, surveillance), environmental impact (e.g., training huge models), fairness considerations (e.g., deployment of technologies that could further disadvantage or exclude historically disadvantaged groups), privacy considerations (e.g., a paper on model/data stealing), and security considerations (e.g., adversarial attacks).
    Consider if the research contributes to overgeneralization, bias confirmation, under or overexposure of specific languages, topics, or applications at the expense of others.
    We expect many papers to be foundational research and not tied to particular applications, let alone deployments. However, we encourage authors to discuss potential risks if they see a path to any positive or negative applications. For example, the authors can emphasize how their systems are intended to be used, how they can safeguard their systems against misuse, or propose future research directions.
    Consider different stakeholders that could be impacted by your work. Consider if it possible that research benefits some stakeholders while harming others. Consider if it pays special attention to vulnerable or marginalized communities. Consider if the research leads to exclusion of certain groups.
    Consider dual use, i.e, possible benefits or harms that could arise when the technology is being used as intended and functioning correctly, benefits or harms that could arise when the technology is being used as intended but gives incorrect results, and benefits or harms following from (intentional or unintentional) misuse of the technology.
    Consider citing previous work on relevant mitigation strategies for the potential risks of the work (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of NLP)."""

supporting_prompt_dict["A3"] = """The main claims in the paper should be clearly stated in the abstract and in the introduction.
    These claims should be supported by evidence presented in the paper, potentially in the form of experimental results, reasoning, or theory. The connection between which evidence supports which claims should be clear.
    The context of the contributions of the paper should be clearly described, and it should be stated how much the results would be expected to generalize to other contexts.
    It should be easy for a casual reader to distinguish between the contributions of the paper and open questions, future work, aspirational goals, motivations, etc."""

supporting_prompt_dict["B1"] = """For composite artifacts like the GLUE benchmark, this means all creators. Cite the original paper that produced the code package or dataset. Remember to state which version of the asset you’re using."""

supporting_prompt_dict["B2"] = """State the name of the license (e.g., CC-BY 4.0) for each asset.
    If you scraped or collected data from a particular source (e.g., website or social media API), you should state the copyright and terms of service of that source.
    Please note that some sources do not allow inference of protected categories like gender, sexual orientation, health status, etc. The data might be in public domain and licensed for research purposes. The data might be used with consent of its creators or copyright holders.
    If the data is used without consent, the paper makes the case to justify its legal basis (e.g., research performed in the public interest under GDPR).
    If you are releasing assets, you should include a license, copyright information, and terms of use in the package.
    If you are repackaging an existing dataset, you should state the original license as well as the one for the derived asset (if it has changed).
    If you cannot find this information online, you are encouraged to reach out to the asset’s creators."""

supporting_prompt_dict["B3"] = """For the artifacts you create, specify the intended use and whether that is compatible with the original access conditions (in particular, derivatives of data accessed for research purposes should not be used outside of research contexts).
    Data and/or pretrained models are released under a specified license that is compatible with the conditions under which access to data was granted (in particular, derivatives of data accessed for research purposes should not be deployed in the real world as anything other than a research prototype, especially commercially).
    The paper specifies the efforts to limit the potential use to circumstances in which the data/models could be used safely (such as an accompanying data/model statement).
    The data is sufficiently anonymized to make identification of individuals impossible without significant effort. If this is not possible due to the research type, please state so explicitly and explain why.
    The paper discusses the harms that may ensue from the limitations of the data collection methodology, especially concerning marginalized/vulnerable populations, and specifies the scope within which the data can be used safely."""

supporting_prompt_dict["B4"] = """There are some settings where the existence of offensive content is not necessarily bad (e.g., swear words occur naturally in text), or part of the research question (i.e., hate speech). This question is just to encourage discussion of potentially undesirable properties.
    Explain how you checked for offensive content and identifiers (e.g., with a script, manually on a sample, etc.).
    Explain how you anonymized the data, i.e., removed identifying information like names, phone and credit card numbers, addresses, user names, etc. Examples are monodirectional hashes, replacement, or removal of data points. If anonymization is not possible due to the nature of the research (e.g., author identification), explain why.
    List any further privacy protection measures you are using: separation of author metadata from text, licensing, etc.
    If any personal data is used: the paper specifies the standards applied for its storage and processing, and any anonymization efforts.
    If the individual speakers remain identifiable via search: the paper discusses possible harms from misuse of this data, and their mitigation."""

supporting_prompt_dict["B5"] = """Scientific artifacts may include code, data, models or other artifacts. Be sure to report the language of any language data, even if it is commonly-used benchmarks.
    Describe basic information about the data that was used, such as the domain of the text, any information about the demographics of the authors, etc."""

supporting_prompt_dict["B6"] = """Even for commonly-used benchmark datasets, include the number of examples in train / validation / test splits, as these provide necessary context for a reader to understand experimental results. For example, small differences in accuracy on large test sets may be significant, while on small test sets they may not be."""

supporting_prompt_dict["C1"] = """Even for commonly-used models like BERT, reporting the number of parameters is important because it provides context necessary for readers to understand experimental results. The size of a model has an impact on performance, and it shouldn’t be up to a reader to have to go look up the number of parameters in models to remind themselves of this information."""

supporting_prompt_dict["C2"] = """The experimental setup should include information about exactly how experiments were set up, like how model selection was done (e.g., early stopping on validation data, the single model with the lowest loss, etc.), how data was preprocessed, etc.
    Many research projects involve manually tuning hyperparameters until some “good” values are found, and then running a final experiment which is reported in the paper. Other projects involve using random search or grid search to find hyperparameters. In all cases, report the results of such experiments, even if they were stopped early or didn’t lead to your best results, as it allows a reader to know the process necessary to get to the final result and to estimate which hyperparameters were important to tune.
    Be sure to include the best-found hyperparameter values (e.g., learning rate, regularization, etc.) as these are critically important for others to build on your work.
    The experimental setup should likely be described in the main body of the paper, as that is important for reviewers to understand the results, but large tables of hyperparameters or the results of hyperparameter searches could be presented in the main paper or appendix."""

supporting_prompt_dict["C3"] = """Error bars can be computed by running experiments with different random seeds, Clopper–Pearson confidence intervals can be placed around the results (e.g., accuracy), or expected validation performance can be useful tools here.
    In all cases, when a result is reported, it should be clear if it is from a single run, the max across N random seeds, the average, etc.
    When reporting a result on a test set, be sure to report a result of the same model on the validation set (if available) so others reproducing your work don’t need to evaluate on the test set to confirm a reproduction."""

supporting_prompt_dict["C4"] = """The version number or reference to specific implementation is important because different implementations of the same metric can lead to slightly different results (e.g., ROUGE).
    The paper cites the original work for the model or software package. If no paper exists, a URL to the website or repository is included.
    If you modified an existing library, explain what changes you made."""

supporting_prompt_dict["D1"] = """Examples of risks include a crowdsourcing experiment which might show offensive content or collect personal identifying information (PII). Ideally, the participants should be warned.
    Including this information in the supplemental material is fine, but if the main contribution of your paper involves human subjects, then we strongly encourage you to include as much detail as possible in the main paper."""

supporting_prompt_dict["D2"] = """Be explicit about how you recruited your participants. For instance, mention the specific crowdsourcing platform used. If participants are students, give information about the population (e.g., graduate/undergraduate, from a specific field), and how they were compensated (e.g., for course credit or through payment).
    In case of payment, provide the amount paid for each task (including any bonuses), and discuss how you determined the amount of time a task would take. Include discussion on how the wage was determined and how you determined that this was a fair wage."""

supporting_prompt_dict["D3"] = """For example, if the was collect via crowdsourcing, the instructions should explain to crowdworkers how the data would be used."""

supporting_prompt_dict["D4"] = """Depending on the country in which research is conducted, ethics review (e.g., from an IRB board in the US context) may be required for any human subjects research. If an ethics review board was involved, you should clearly state it in the paper. However, stating that you obtained approval from an ethics review board does not imply that the societal impact of the work does not need to be discussed.
    For initial submissions, do not include any information that would break anonymity, such as the institution conducting the review."""

supporting_prompt_dict["D5"] = """State if your data include any protected information (e.g., sexual orientation or political views under GDPR).
    The paper is accompanied by a data statement describing the basic demographic and geographic characteristics of the author population that is the source of the data, and the population that it is intended to represent.
    If applicable: the paper describes whether any characteristics of the human subjects were self-reported (preferably) or inferred (in what way), justifying the methodology and choice of description categories."""

def generate_prompt_dict_acl(prompt_instruction, prompt_instruction_A3, combined_node_id):
    prompt_dict = OrderedDict()

    ## A for Every Submission
    ###
    prompt_dict["A1"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you describe the limitations of your work?
    Additional Context: {supporting_prompt_dict["A1"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["A2"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you discuss any potential risks of your work?
    Additional Context: {supporting_prompt_dict["A2"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["A3"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Does the {combined_node_id} summarize the paper’s main claims?
    Additional Context: {supporting_prompt_dict["A3"]}
    Output Structure: """ + prompt_instruction_A3

    ## B Did you use or create scientific artifacts?
    ###
    prompt_dict["B1"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference. Scientific artifacts may include code, data, models or other artifacts.
    Question: Did you cite the creators of artifacts you used?
    #Additional Context: {supporting_prompt_dict["B1"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["B2"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference. Scientific artifacts may include code, data, models or other artifacts.
    Question: Did you discuss the license or terms for use and/or distribution of any scientific artifacts?
    Additional Context: {supporting_prompt_dict["B2"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["B3"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference. Scientific artifacts may include code, data, models or other artifacts.
    Question: Did you discuss if your use of existing artifact(s) was consistent with their intended use, provided that it was specified?
    Additional Context: {supporting_prompt_dict["B3"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["B4"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you discuss the steps taken to check whether the data that was collected / used contains any information that names or uniquely identifies individual people or offensive content, and the steps taken to protect / anonymize it?
    Additional Context: {supporting_prompt_dict["B4"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["B5"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Scientific artifacts may include code, data, models or other artifacts. Question: Did you provide documentation of the artifacts, e.g., coverage of domains, languages, and linguistic phenomena, demographic groups represented, etc.?
    Additional Context: {supporting_prompt_dict["B5"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["B6"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Did you report relevant statistics like the number of examples, details of train / test / dev splits, etc. for the data that you used / created?
    Additional Context: {supporting_prompt_dict["B6"]}
    Output Structure: """ + prompt_instruction

    ## C Did you run computational experiments
    ###
    prompt_dict["C1"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you report the number of parameters in the models used, the total computational budget (e.g., GPU hours), or computing infrastructure used?
    Additional Context: {supporting_prompt_dict["C1"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["C2"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you discuss the experimental setup, including hyperparameter search and best-found hyperparameter values?
    Additional Context: {supporting_prompt_dict["C2"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["C3"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you report descriptive statistics about your results (e.g., error bars around results, summary statistics from sets of experiments), and is it transparent whether you are reporting the max, mean, etc. or just a single run?
    Additional Context: {supporting_prompt_dict["C3"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["C4"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: If you used existing packages (e.g., for preprocessing, for normalization, or for evaluation), did you report the implementation, model, and parameter settings used (e.g., NLTK, Spacy, ROUGE, etc.)?
    Additional Context: {supporting_prompt_dict["C4"]}
    Output Structure: """ + prompt_instruction

    ## D Did you use human annotators (e.g., crowdworkers) or research with human participants?
    ###
    prompt_dict["D1"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you report the full text of instructions given to participants, including e.g., screenshots, disclaimers of any risks to participants or annotators, etc.?
    Additional Context: {supporting_prompt_dict["D1"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["D2"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you report information about how you recruited (e.g., crowdsourcing platform, students) and paid participants, and discuss if such payment is adequate given the participants’ demographic (e.g., country of residence)?
    Additional Context: {supporting_prompt_dict["D2"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["D3"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you discuss whether and how consent was obtained from people whose data you’re using/curating?
    Additional Context: {supporting_prompt_dict["D3"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["D4"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Was the data collection protocol approved (or determined exempt) by an ethics review board?
    Additional Context: {supporting_prompt_dict["D4"]}
    Output Structure: """ + prompt_instruction

    prompt_dict["D5"] = f"""Introduction: Behave like you are the author of a paper you are going to submit to a conference.
    Question: Did you report the basic demographic and geographic characteristics of the annotator population that is the source of the data?
    Additional Context: {supporting_prompt_dict["D5"]}
    Output Structure: """ + prompt_instruction

    ## E Did you use AI assistants (e.g., ChatGPT, Copilot) in your research, coding, or writing?
    ###

    # E1. Did you include information about your use of AI assistants?

    # E1. Elaboration For Yes Or No. For yes, provide a section number. For no, justify why not.

    # E1. Section Or Justification

    return prompt_dict

# Export supporting_prompt_dict
__all__ = ['generate_prompt_dict_acl']
