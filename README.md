<p align="center">
  <img src="https://i.ibb.co/0hfQZpd/aclready-logo.png" alt="ACLReady's Logo"/>
</p>

<p align="center">A simple tool to parse your paper, help fill the ACL responsible checklist, and reducing the likelihood of desk rejection.</p>
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

- is <b>an easy-to-use Llama powered web interface</b> which automates the daunting process of filling out an overlong conference specific checklist. If you want to save time, reduce effort and minimze the risk of getting desk rejected, you can use this tool to compliment and aid your research journey.
- is <b>highly flexible</b> and offers various adaptions and possibilities such as
prompt customization, thereby, enabling developers continue develop this tool for other conferences.

## Installation
To install and run the web interface or UI:
```
git clone git@github.com:gtfintechlab/ACL_SystemDemonstrationChecklist.git
cd ACL_SystemDemonstrationChecklist
cd aclready
npm install
npm start
```

To install and run the python server:
```
cd server
python3 server.py
```

## Basic Concepts

ACLReady aims to reduce the time and effort required by a researcher to fill the ACL Responsible NLP Research Checklist. Without taking away the freedom of the researcher to edit the checklist manually, we intend to ease this process through different mechanisms: an interative web interface, a language model and a generator:
- <b>Interactive Web Interface</b>: A web interface with a sleek design entices the author to upload his/her research paper and analyse its issues with minimal effort.
- <b>LLM</b>: We use [Together AI](https://www.together.ai) as our LLM interface. Together AI
supports a wide range of LLMs including Llama, Mixtral Instruct, QWEN 1.5 ,and many more.