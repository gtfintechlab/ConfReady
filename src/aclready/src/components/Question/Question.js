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
  }, [initialResponse.text, initialResponse.choice]);

  const handleResponseChange = (e) => {
    const newResponse = e.target.value;
    setResponse(newResponse);
    dispatch({ type: 'SET_RESPONSE', payload: { id, response: { choice, text: newResponse }}});
  };

  const handleChoiceChange = (newChoice) => {
    setChoice(newChoice);
    dispatch({ type: 'SET_RESPONSE', payload: { id, response: { choice: newChoice, text: response } } });
  };

  return (
    <div className='w-full flex flex-col mb-6' id={id}>
      {!isRoot && (
        <div className='flex flex-row justify-between items-center'>
        <h1 className='text-xl my-4'><b>{id}</b>&nbsp;&nbsp;|&nbsp;&nbsp;{question_data}</h1>
        <div className='bg-gray-500 flex flex-row w-fit rounded-full mb-5 h-fit ml-4'>
        <h1 className={`px-4 py-2 cursor-pointer text-white ease-in duration-300 rounded-full ${choice ? "bg-gray-700" : "bg-gray-500"}`}
            onClick={() => handleChoiceChange(true)}>YES</h1>
        <h1 className={`px-4 py-2 cursor-pointer text-white ease-in duration-300 rounded-full ${!choice ? "bg-gray-700" : "bg-gray-500"}`}
            onClick={() => handleChoiceChange(false)}>NO</h1>
      </div>
        </div>
      )}
      {
        isRoot ? (
          <div className='flex flex-row justify-between mb-10'>
            <p className='text-lg mb-4 mt-4'>If you answer <b>Yes</b>, answer the questions below; if you answer <b>No</b>, you can skip the rest of this section.</p>
            <div className='bg-gray-500 flex flex-row w-fit rounded-full mb-5 h-fit ml-4'>
            <h1 className={`px-4 py-2 cursor-pointer text-white ease-in duration-300 rounded-full ${choice ? "bg-gray-700" : "bg-gray-500"}`}
            onClick={() => handleChoiceChange(true)}>YES</h1>
        <h1 className={`px-4 py-2 cursor-pointer text-white ease-in duration-300 rounded-full ${!choice ? "bg-gray-700" : "bg-gray-500"}`}
            onClick={() => handleChoiceChange(false)}>NO</h1>
      </div>
      </div>
        ) : (
            <p className='text-lg mb-4'>If you answer <b>Yes</b>, provide the section number; if you answer <b>No</b>, provide a justification.</p>
        )
      }
      {!isRoot && (
        <textarea className='text-black border-gray-200 h-24 border-2 rounded p-2 outline-none'
                  placeholder={`${choice ? 'Mention section number and elucidate on it...' : 'Mention Justification ...'}`}
                  value={response}
                  onChange={handleResponseChange} />
      )}
    </div>
  );
}

export default Question;
