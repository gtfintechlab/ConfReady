import React, { useState, useEffect } from 'react';
import { useStore } from '../../store';

function Question({ id, question_data, isRoot }) {
  const { state, dispatch } = useStore();
  const { responses } = state;
  const initialResponse = responses[id] || { choice: false, text: '' };
  const [response, setResponse] = useState(initialResponse.text);
  const [choice, setChoice] = useState(initialResponse.choice);

  useEffect(() => {
    setResponse(initialResponse.text);
    setChoice(initialResponse.choice);
  }, [id, initialResponse.text, initialResponse.choice]);

  const handleResponseChange = (e) => {
    const newResponse = e.target.value;
    setResponse(newResponse);
    dispatch({ type: 'SET_RESPONSE', payload: { id, response: { choice, text: newResponse } } });
  };

  const handleChoiceChange = (newChoice) => {
    setChoice(newChoice);
    dispatch({ type: 'SET_RESPONSE', payload: { id, response: { choice: newChoice, text: response } } });
  };

  return (
    <div className='w-full flex flex-col mb-6' id={id}>
      {!isRoot && (
        <h1 className='times text-xl my-4'><b>{id}</b>&nbsp;&nbsp;&nbsp;&nbsp;{question_data}</h1>
      )}
      {
        isRoot ? (
            <p className='times text-lg mb-4'>If you answer <b>Yes</b>, answer the questions below; if you answer <b>No</b>, you can skip the rest of this section.</p>
        ) : (
            <p className='times text-lg mb-4'>If you answer <b>Yes</b>, provide the section number; if you answer <b>No</b>, provide a justification.</p>
        )
      }
      <div className='bg-gray-200 flex flex-row w-fit rounded-full mb-5'>
        <h1 className={`times mx-4 my-2 cursor-pointer text-gray-900 ease-in duration-300 hover:text-gray-600 ${choice ? "font-bold" : ""}`}
            onClick={() => handleChoiceChange(true)}>Yes</h1>
        <h1 className={`times mx-4 my-2 cursor-pointer text-gray-900 ease-in duration-300 hover:text-gray-600 ${!choice ? "font-bold" : ""}`}
            onClick={() => handleChoiceChange(false)}>No</h1>
      </div>
      {!isRoot && (
        <textarea className='text-black border-gray-200 h-24 border-2 rounded p-2 times outline-none'
                  placeholder='Section or Justification...'
                  value={response}
                  onChange={handleResponseChange} />
      )}
    </div>
  );
}

export default Question;
