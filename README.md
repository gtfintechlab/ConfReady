<p align="center">
  <img src="confready/public/confready.png" alt="ConfReady's Logo" width="300"/>
</p>

<p align="center">A simple tool to parse your paper and assist with conference checklists.</p>
<p align="center"><em>Accepted at EMNLP Demonstrations 2025</em></p>

<p align="center">
<img alt="version" src="https://img.shields.io/badge/version-0.2.0-green">
<img alt="python" src="https://img.shields.io/badge/python-3.11-blue">
<img alt="license" src="https://img.shields.io/badge/license-AGPL%20v3-blue">
</p>
<div align="center">
<hr>

<p align="center">
  <a href="https://www.linkedin.com/in/michaelgalarnyk/">Michael Galarnyk*</a>,
  <a href="https://www.linkedin.com/in/rutwikroutu/">Rutwik Routu*</a>,
  <a href="https://www.linkedin.com/in/vidhyakshayakannan/">Vidhyakshaya Kannan*</a>,
  <a href="https://www.linkedin.com/in/koshabheda/">Kosha Bheda</a>,<br/>
  <a href="https://www.linkedin.com/in/prasunbanerjee04/">Prasun Banerjee</a>,
  <a href="https://shahagam4.github.io/">Agam Shah</a>,
  <a href="https://www.scheller.gatech.edu/directory/faculty/chava/index.html">Sudheer Chava</a><br/>
Georgia Institute of Technology<br/>
</p>

<p align="center"><em>*Authors contributed equally</em></p>

[Installation](#installation) | [Documentation](https://confready-docs.vercel.app/docs/introduction)

<hr>
</div>

## Overview

This repository:

- is **an easy-to-use Llama or GPT powered web interface** which can be used to empower authors to reflect on their work and assist authors with conference checklists
- is **highly flexible** and offers various adaptations and possibilities such as prompt customization, enabling developers to continue developing this tool for additional conferences

An overview of ConfReady is presented in this [YouTube video](https://www.youtube.com/watch?v=sNhpKJLfArc).

## Installation

You can install ConfReady in two ways.

### Prerequisites

- Python 3.11+
- [NPM (Node.js](https://nodejs.org/). This is required for the web interface.

### PyPy (Recommended)

```
pip install confready
```

### GitHub Installation Steps

1. **Clone the repository** and navigate to the project directory:

    ```bash
    git clone https://github.com/gtfintechlab/ConfReady.git
    cd ConfReady
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
    cd confready
    npm start
    ```

3. **Access the API**:

    The server will be running on `http://localhost:3000/`.
   
## Documentation

We welcome contributions to this library and encourage potential contributors to start by reviewing our [documentation](https://confready-docs.vercel.app/docs/introduction) to familiarize themselves with the codebase's format and structure. Once you have a solid understanding, feel free to submit a pull request. We’re excited to collaborate with new contributors and drive this project forward together.

## Citation

Coming soon!

```bibtex

```
