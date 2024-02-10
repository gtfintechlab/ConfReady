"use client"

import { useRef } from 'react';
import {useModelStore} from '../../store';

export default function ModelCardGenerator() {

    const modelStore = useModelStore();

    const tempMarkdown = modelStore.tempMarkdown;
    const provideCode = modelStore.provideCode;
    const name = modelStore.name;
    const authors = modelStore.authors;
    const provideData = modelStore.provideData;
    const datasetSummary = modelStore.datasetSummary;

    const nameRef = useRef(null);
    const authorsRef = useRef(null);
    const datasetSummaryRef = useRef(null);
    const provideCodeRef = useRef(null);
    const provideDataRef = useRef(null);

    function generateMarkdown() {

      const nameValue = nameRef.current.value;
      const authorsValue = authorsRef.current.value;
      const provideDatasetSummaryValue = datasetSummaryRef.current.value;
      const provideCodeValue = provideCodeRef.current.value;
      const provideDataValue = provideDataRef.current.value;

      modelStore.setName(nameValue);
      modelStore.setAuthors(authors);
      modelStore.setDatasetSummary(provideDatasetSummaryValue);
      modelStore.setProvideData(provideDataValue);
      modelStore.setProvideCode(provideCodeValue);
      
        const markdownTemplate = `
        ---
license: cc-by-nc-4.0
task_categories:
language:
- en
pretty_name:
size_categories:
multilinguality:
- monolingual
task_ids:
---
# Dataset Card for "${nameValue}"

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
  - [Languages](#languages)
- [Dataset Creation and Annotation](#dataset-creation)
- [Additional Information](#additional-information)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)
  - [Contact Information](#contact-information)

## Dataset Description

- **Homepage:** [${provideDataValue}](${provideDataValue})
- **Paper:** [Arxiv Link]()

### Dataset Summary

${provideDatasetSummaryValue}

For more details check [information in paper]()

### Supported Tasks and Leaderboards

[More Information Needed](https://github.com/huggingface/datasets/blob/master/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)

### Languages

- It is a monolingual English dataset

## Dataset Creation and Annotation


[Information in paper ]()


## Additional Information


### Licensing Information

[Information in paper ]()


### Contact Information

Please contact ${authorsValue} about any ${nameValue}-related issues and questions.
        
        `

        modelStore.setTempMarkdown(markdownTemplate);
        nameRef.current.value = '';
        authorsRef.current.value = '';
      datasetSummaryRef.current.value = '';
      provideCodeRef.current.value = '';
      provideDataRef.current.value = '';
      }

    return (
        <div className="bg-zinc-100 px-4 md:px-8 flex flex-col items-center">
  <div className="container mx-auto px-4 md:px-8 max-w-2xl flex flex-col items-center mt-10">
    {/* Adjust spacing and other styles as needed within these classes */}
    <h1 className="text-2xl font-light text-center">Build your Model Card</h1>
    <hr className="my-5 w-full" />

    <div className="w-full flex flex-col items-center gap-8">
      {/* Form fields with more spacious layout and larger inputs */}
      <div className="flex flex-col w-full">
        <h3 className="mb-2">Name of Research Paper</h3>
        <input
          placeholder="Enter the name of the research paper"
          className="border-none outline-none py-3 px-12 rounded w-full h-fit"
          ref={nameRef}
        />
      </div>

      <div className="flex flex-col w-full">
        <h3 className="mb-2">Who are the authors? (Last Name, First Name)</h3>
        <input
          placeholder="Enter the name of the research paper"
          className="border-none outline-none py-3 px-12 rounded w-full h-fit"
          ref={authorsRef}
        />
      </div>

      <div className="flex flex-col w-full">
        <h3 className="mb-2">Do you provide code? (Yes/No)</h3>
        <input
          placeholder="Enter the name of the research paper"
          className="border-none outline-none py-3 px-12 rounded w-full h-fit"
          ref={provideCodeRef}
        />
      </div>

      <div className="flex flex-col w-full">
        <h3 className="mb-2">Do you provide data? If so, where is it stored?</h3>
        <input
          placeholder="Enter the name of the research paper"
          className="border-none outline-none py-3 px-12 rounded w-full h-fit"
          ref={provideDataRef}
        />
      </div>
      
      <div className="flex flex-col w-full">
        <h3 className="mb-2">Do you provide data? If so, where is it stored?</h3>
        <input
          placeholder="Enter the name of the research paper"
          className="border-none outline-none py-3 px-12 rounded w-full h-fit"
          ref={datasetSummaryRef}
        />
      </div>

      <button
        className="mb-10 font-normal w-full bg-slate-400 hover:bg-slate-500 text-white font-bold py-3 px-8 rounded"
        onClick={() => generateMarkdown()}
      >
        Export to Markdown
      </button>
    </div>
  </div>
</div>

    )
}