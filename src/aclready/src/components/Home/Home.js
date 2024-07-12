import React from 'react';
import Sidebar from '../Sidebar/Sidebar';
import Question from '../Question/Question';
import { useStore } from '../../store';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import DownloadIcon from '@mui/icons-material/Download';
import { motion, AnimatePresence } from 'framer-motion';


function Home() {
  const { state, dispatch } = useStore();
  const { responses, aclQuestions, currentStage, sectionProgress } = state;
  const listHeader = ['A', 'B', 'C', 'D', 'E'];

  return (
    <>
      {/* <div className='bg-gray-100 h-fit fixed right-0 flex flex-col p-5 mr-5 rounded-full top-1/2 mt-[-70px] shadow-lg'>
        {['A', 'B', 'C', 'D', 'E'].map(stage => (
          <p key={stage}
             className={`text-xl font-semibold ${currentStage == stage ? "text-black" : "text-gray-400"} cursor-pointer ease-in duration-300 hover:text-gray-600`}
             onClick={() => dispatch({ type: 'SET_CURRENT_STAGE', payload: stage })}>
            {stage}
          </p>
        ))}
      </div> */}
      <Sidebar />
      <div className='absolute height-fultop-0 bottom-72 w-full' />
      <div className="p-4 sm:ml-72 mt-10">
        <div className='rounded mr-5'>
          {aclQuestions && aclQuestions.map(({ id, quest }) => {
            if (id == currentStage) {
              return (
                <div key={id}>
                  <h1 className='text-3xl mb-4 text-center font-thin'><b>SECTION {id}</b></h1>
                  <div className='w-full flex align-center justify-center'>
                  <div className='flex ease-in duration-300 justify-center items-center bg-gray-500 w-fit rounded-full'>
        {listHeader.map(stage => (
          <div
          key={stage}
          className={`flex items-center text-xl py-1 font-semibold px-3 ${currentStage === stage ? 'bg-gray-700 text-white opacity-100' : 'bg-gray-500 text-white opacity-50'} rounded-full cursor-pointer`}
          onClick={() => dispatch({ type: 'SET_CURRENT_STAGE', payload: stage })}
          style={{ transition: 'all 0.3s ease-in-out' }} // Add transition here
        >
            {stage}
            {/* <progress
              className='mx-4 rounded-lg'
              value={sectionProgress[stage] || 0}
              max="100"
            ></progress> */}
            <div className="relative h-1 bg-gray-400 rounded-full overflow-hidden mx-4 w-24">
              <div
                className="progress-bar h-1 bg-white z-10"
                style={{ width: `${sectionProgress[stage] || 0}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
      </div>
      <div className='p-24 pb-10 pt-12'>
                  <h1 className='times text-2xl font-bold'>{id} | <span className='font-normal'>{quest.title}</span></h1>
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
                </div>
              );
            }
            return null;
          })}
        </div>
        <div className='flex flex-row justify-between px-10 align-center mb-10'>
            <button onClick={() => {
              const listHeader = ['A', 'B', 'C', 'D', 'E'];
          let nextIndex = (listHeader.indexOf(currentStage) - 1);
          if(nextIndex < 0) nextIndex = 0;
          dispatch({ type: 'SET_CURRENT_STAGE', payload: listHeader[nextIndex] })
            }} className={`flex flex-row items-center justify-center text-lg ${currentStage == 'A' && 'opacity-20'}`}><ArrowBackIosNewIcon />&nbsp;&nbsp;Previous Section</button>
            
            <button className={`relative right-0 ${currentStage == 'E' && 'hidden'} text-lg`} onClick={() => {
              const listHeader = ['A', 'B', 'C', 'D', 'E'];
              let nextIndex = (listHeader.indexOf(currentStage) + 1);
              dispatch({ type: 'SET_CURRENT_STAGE', payload: listHeader[nextIndex] })
            }}>Next Section&nbsp;&nbsp;<ArrowForwardIosIcon /></button>
            {
          currentStage == 'E' && (
            <button className='bg-black text-white p-3 rounded-full'>Download Document&nbsp;&nbsp;<DownloadIcon /></button>
          )
        }
          </div>
      </div>
    </>
  );
}

export default Home;
