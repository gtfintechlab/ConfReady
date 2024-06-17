<p align="center">
  <img src="https://i.ibb.co/0hfQZpd/aclready-logo.png" alt="ACLReady's Logo"/>
</p>

<p align="center">A simple tool to parse your paper, help fill the ACL responsible checklist, and reduce the likelihood of desk rejection.</p>
<p align="center">
<img alt="version" src="https://img.shields.io/badge/version-0.1.0-green">
<img alt="python" src="https://img.shields.io/badge/python-3.10-blue">
<img alt="Static Badge" src="https://img.shields.io/badge/license-MIT-green">
</p>
<div align="center">
<hr>

[Installation](#installation) | [Basic Concepts](#basic-concepts)

<hr>
</div>

## Overview

This repository:

- is **an easy-to-use Llama powered web interface** which automates the daunting process of filling out an overlong conference specific checklist. If you want to save time, reduce effort and minimize the risk of getting desk rejected, you can use this tool to complement and aid your research journey.
- is **highly flexible** and offers various adaptations and possibilities such as prompt customization, thereby, enabling developers to continue developing this tool for other conferences.

## Installation

### Prerequisites

- Conda (Miniconda or Anaconda)
- Node.js (npm)

### Steps

1. **Clone the repository** and navigate to the project directory:

    ```bash
    git clone git@github.com:gtfintechlab/ACL_SystemDemonstrationChecklist.git
    cd ACL_SystemDemonstrationChecklist
    cd aclready
    ```

2. **Create and activate the conda environment**:

    ```bash
    conda env create -f environment.yml
    conda activate aclready_env
    ```

3. **Install npm dependencies**:

    ```bash
    npm install
    ```

4. **Add your API keys**:

    - Create a `.env` file inside the `server` directory:

    ```ini
    TOGETHERAI_API_KEY=your_together_ai_key_here
    OPENAI_API_KEY=your_openai_key_here
    ```

5. **Run the Flask server**:

    ```bash
    cd server
    python server.py
    ```

6. **Run the Web Interface**:

    ```bash
    cd aclready
    npm start
    ```

7. **Access the API**:

    The server will be running on `http://localhost:8080`.

### Folder Structure

```
aclready/
├── environment.yml
├── client/
│   └── (client-side files)
├── server/
│   ├── server.py
│   └── .env
└── README.md
```

## Basic Concepts

ACLReady aims to reduce the time and effort required by a researcher to fill the ACL Responsible NLP Research Checklist. Without taking away the freedom of the researcher to edit the checklist manually, we intend to ease this process through different mechanisms: an interactive web interface, a language model, and a generator:

- **Interactive Web Interface**: A web interface with a sleek design entices the author to upload his/her research paper and analyze its issues with minimal effort.
- **LLM**: We use [Together AI](https://www.together.ai) as our LLM interface. Together AI supports a wide range of LLMs including Llama, Mixtral Instruct, QWEN 1.5, and many more.