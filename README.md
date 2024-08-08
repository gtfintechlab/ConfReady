<p align="center">
  <img src="https://i.ibb.co/0hfQZpd/aclready-logo.png" alt="ACLReady's Logo"/>
</p>

<p align="center">A simple tool to parse your paper and help fill the ACL responsible checklist.</p>
<p align="center">
<img alt="version" src="https://img.shields.io/badge/version-0.1.0-green">
<img alt="python" src="https://img.shields.io/badge/python-3.11-blue">
<img alt="Static Badge" src="https://img.shields.io/badge/license-MIT-green">
</p>
<div align="center">
<hr>

[Installation](#installation) | [Citation](#citation)

<hr>
</div>

## Overview

This repository:

- is **an easy-to-use GPT 3.5 or Llama powered web interface** which can help fill in the ACL checklist. If you want to save time and reduce effort, check out this tool to complement and aid your research journey.
- is **highly flexible** and offers various adaptations and possibilities such as prompt customization, thereby, enabling developers to continue developing this tool for other conferences.

An overview of ACLReady is presented in this [YouTube video](https://youtu.be/_V0OV2E90FY?si=2v2rlx5T2dQzWK8L).

## Installation

### Prerequisites

- Conda (Miniconda or Anaconda)

### Steps

1. **Clone the repository** and navigate to the project directory:

    ```bash
    git clone https://github.com/gtfintechlab/ACLReady.git
    cd ACLReady
    ```

2. **Run the installation script**:

    ```bash
   source install.sh
    ```

3. **Add your API keys**:

    - Add LLM inference provider API keys to the .env file inside the `server` directory.

    ```ini
    TOGETHERAI_API_KEY=your_together_ai_key_here
    OPENAI_API_KEY=your_openai_key_here
    ```

## Run the App
1. **Run the Flask server**:

    ```bash
    cd server
    python app.py
    ```

2. **Run the Web Interface**:

    ```bash
    cd aclready
    npm start
    ```

3. **Access the API**:

    The server will be running on `http://localhost:3000/`.

## Citation

If you find this repository useful, please cite our work (soon to be on arxiv).


