import React from 'react';
import Sidebar from '../Sidebar/Sidebar';
import Question from '../Question/Question';
import { useStore } from '../../store';

function Home() {
  const { state, dispatch } = useStore();
  const { responses, aclQuestions, currentStage } = state;

  return (
    <>
      <div className='bg-gray-100 h-fit fixed right-0 flex flex-col p-5 mr-5 rounded-full top-1/2 mt-[-70px] shadow-lg'>
        {['A', 'B', 'C', 'D', 'E'].map(stage => (
          <p key={stage}
             className={`text-xl font-semibold ${currentStage == stage ? "text-black" : "text-gray-400"} cursor-pointer ease-in duration-300 hover:text-gray-600`}
             onClick={() => dispatch({ type: 'SET_CURRENT_STAGE', payload: stage })}>
            {stage}
          </p>
        ))}
      </div>
      <Sidebar />
      <div className='absolute height-fultop-0 bottom-72 w-12' />
      <div className="p-4 sm:ml-72 mt-20">
        <div className='w-11/12 rounded'>
          {aclQuestions && aclQuestions.map(({ id, quest }) => {
            if (id == currentStage) {
              return (
                <div key={id}>
                  <h1 className='times font-medium text-3xl mb-4'>{id}&nbsp;&nbsp;&nbsp;&nbsp;{quest.title}</h1>
                  {quest.titleResponse == 1 && (
                    <Question key={id} id={id} question_data={null} isRoot={true} />
                  )}
                  {responses[id] != null && responses[id].choice == true && Object.entries(quest.questions)
                    .sort((a, b) => {
                      const numA = parseInt(a[0].slice(1), 10);
                      const numB = parseInt(b[0].slice(1), 10);
                      return numA - numB;
                    })
                    .map(([id2, question_data]) => (
                      <div key={id2}>
                        <Question id={id2} question_data={question_data} isRoot={false} className="mt-10" />
                        <hr className='my-6' />
                      </div>
                    ))}

                    {quest.titleResponse == 0 && Object.entries(quest.questions)
                    .sort((a, b) => {
                      const numA = parseInt(a[0].slice(1), 10);
                      const numB = parseInt(b[0].slice(1), 10);
                      return numA - numB;
                    })
                    .map(([id2, question_data]) => (
                      <div key={id2}>
                        <Question id={id2} question_data={question_data} isRoot={false} className="mt-10" />
                        <hr className='my-6' />
                      </div>
                    ))}
                </div>
              );
            }
            return null;
          })}
        </div>
      </div>
    </>
  );
}

export default Home;
