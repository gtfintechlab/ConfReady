"use client"

import ReactMarkdown from 'react-markdown';
import githubMarkdownCss from 'github-markdown-css';
import Highlight from 'react-highlight';
import {useModelStore} from '../../store';

function ModelCardPreview() {
    const modelStore = useModelStore();

    const tempMarkdown = modelStore.tempMarkdown;
    const provideCode = modelStore.provideCode;
    const name = modelStore.name;
    const authors = modelStore.authors;
    const provideData = modelStore.provideData;

    function downloadMarkdown() {
        const blob = new Blob([tempMarkdown], { type: 'text/plain;charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'model-card.md';
        link.click();
      }

  return (
    <div className="markdown-preview">
      {tempMarkdown && (
        <div className="container mx-auto px-4 rounded-lg bg-white shadow-md overflow-auto">
          <h2 className="text-xl font-semibold my-4 px-4">Preview</h2>
          <pre className="markdown-content">
            {tempMarkdown}
          </pre>
          <button
            className="my-5 w-full bg-slate-400 hover:bg-slate-500 text-white font-bold py-3 px-8 rounded"
            onClick={downloadMarkdown}
          >
            Download Markdown
          </button>
        </div>
      )}
    </div>
  )
}

export default ModelCardPreview