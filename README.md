<p align="center">
  <img src="https://i.ibb.co/0hfQZpd/aclready-logo.png" alt="ACLReady's Logo"/>
</p>

<p align="center">A simple tool to parse your paper and help fill the ACL responsible checklist.</p>
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

- is **an easy-to-use Llama powered web interface** which helps fill in the ACL checklist. If you want to save time and reduce effort, check out this tool to complement and aid your research journey.
- is **highly flexible** and offers various adaptations and possibilities such as prompt customization, thereby, enabling developers to continue developing this tool for other conferences.

## Installation

### Prerequisites

- Conda (Miniconda or Anaconda)

### Steps

1. **Clone the repository** and navigate to the project directory:

    ```bash
    git clone git@github.com:gtfintechlab/ACL_SystemDemonstrationChecklist.git
    cd ACL_SystemDemonstrationChecklist
    ```

2. **Create and activate the conda environment**:

    ```bash
   source install.sh
    ```

3. **Add your API keys**:

    - Add whatever LLM inference provider API keys to the .env file inside the `server` directory:

    ```ini
    TOGETHERAI_API_KEY=your_together_ai_key_here
    OPENAI_API_KEY=your_openai_key_here
    ```

## Run the App
1. **Run the Flask server**:

    ```bash
    cd server
    python server.py
    ```

2. **Run the Web Interface**:

    ```bash
    cd aclready
    npm start
    ```

3. **Access the API**:

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