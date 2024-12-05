import React, { useEffect, useState } from 'react';
import Sidebar from '../Sidebar/Sidebar';
import Question from '../Question/Question';
import { useStore } from '../../store';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import DownloadIcon from '@mui/icons-material/Download';
import { saveAs } from 'file-saver';

function Home() {
  const { state, dispatch } = useStore();
  const { responses, confQuestions, currentStage, sectionProgress, timeTaken, checklistName, llmGenerated } = state;
  const [listHeader, setListHeader] = useState(['A', 'B', 'C', 'D', 'E']);

  useEffect(() => {
    if(checklistName == 'aclchecklist') {
      setListHeader(['A', 'B', 'C', 'D', 'E'])
    } else if(checklistName == 'neurips-checklist-a') {
      setListHeader(['1', '2', '3', '4', '5'])
    } else if(checklistName == 'neurips-checklist-b') {
      setListHeader(['1', '2'])
    }
  }, [checklistName])

  useEffect(() => {
    confQuestions.forEach(({id, quest}) => {
      Object.keys(quest.questions).sort((a, b) => {
        const numA = parseInt(a.slice(1), 10);
        const numB = parseInt(b.slice(1), 10);
        return numA - numB;
      })
      .forEach(questionId => {
        const response = responses[questionId];
        console.log(response)
      //   console.log(response.s_name)
      })
    })
  }, [])

  const generateMarkdown = () => {
    let markdown = "# ACL Responsible Checklist Responses\n\n";
    if(timeTaken) {
      markdown += `${timeTaken}\n\n`
    }

    confQuestions.forEach(({ id, quest }) => {
      markdown += `## Section ${id}: ${quest.title}\n\n`;

      Object.keys(quest.questions).sort((a, b) => {
        const numA = parseInt(a.slice(1), 10);
        const numB = parseInt(b.slice(1), 10);
        return numA - numB;
      }).forEach(questionId => {
        const questionText = quest.questions[questionId];
        const response = responses[questionId];

        if (response) {
          markdown += `### ${questionId}: ${questionText}\n`;
          markdown += `**Yes/No:** ${response.choice == true ? 'Yes' : 'No'}\n\n`
          markdown += `**Response:** ${response.text}\n\n`;
        } else {
          markdown += `### ${questionId}: ${questionText}\n`;
          markdown += `**Response:** No response provided.\n\n`;
        }
      });
    });

    return markdown;
  };

  const handleDownload = () => {
    const markdownContent = generateMarkdown();
    const blob = new Blob([markdownContent], { type: 'text/markdown;charset=utf-8' });
    saveAs(blob, 'acl_responses.md');
  };

  const handleScroll = () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    
    if (scrollTop + clientHeight === scrollHeight) {
      // Dispatch action to set bottomReached for current section
      dispatch({ type: 'SET_BOTTOM_REACHED', payload: { section: currentStage, value: 1 } });
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [currentStage]); // Re-attach when currentStage changes
  

  return (
    <>
      <Sidebar />
      <div className='absolute height-fultop-0 bottom-72 w-full' />
      <div className="p-4 sm:ml-72 mt-10">
        <div className='rounded mr-5'>
          {confQuestions && confQuestions.map(({ id, quest }) => {
            if (id == currentStage) {
              return (
                <div key={id}>
                  <h1 className='text-3xl mb-6 text-center font-thin'><b>SECTION {id}</b></h1>
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
      <div className='p-24 pb-10 pt-20'>
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
                        <hr className='my-6 mb-14' />
                      </div>
                    ))}

{
  quest.titleResponse == 0 && Object.entries(quest.questions)
    .sort((a, b) => {
      const extractParts = (key) => {
        const match = key.match(/^(\d+)\.\s*\((\w)\)|^([A-Za-z])(\d+)$/);
        if (match) {
          if (match[1]) {
            return [parseInt(match[1], 10), match[2]];
          } else {
            return [parseInt(match[4], 10), match[3]];
          }
        }
        return [Infinity, ''];
      };

      const [numA, subA] = extractParts(a[0]);
      const [numB, subB] = extractParts(b[0]);
      if (numA !== numB) return numA - numB;
      return subA.localeCompare(subB);
    })
    .map(([id2, question_data]) => (
      <div key={id2}>
        <Question id={id2} question_data={question_data} isRoot={false} className="mt-10" />
        <hr className='my-6 mb-14' />
      </div>
    ))
}

                    </div>
                </div>
              );
            }
            return null;
          })}
        </div>
        <div className='flex flex-row justify-between px-10 align-center mb-10'>
            <button onClick={() => {
          let nextIndex = (listHeader.indexOf(currentStage) - 1);
          if(nextIndex < 0) nextIndex = 0;
          dispatch({ type: 'SET_CURRENT_STAGE', payload: listHeader[nextIndex] })
            }} className={`flex flex-row items-center justify-center text-lg ${currentStage == listHeader[0] && 'opacity-20'}`}><ArrowBackIosNewIcon />&nbsp;&nbsp;Previous Section</button>
            
            <button className={`relative right-0 ${currentStage == listHeader[listHeader.length - 1] && 'hidden'} text-lg`} onClick={() => {
              let nextIndex = (listHeader.indexOf(currentStage) + 1);
              dispatch({ type: 'SET_CURRENT_STAGE', payload: listHeader[nextIndex] })
            }}>Next Section&nbsp;&nbsp;<ArrowForwardIosIcon /></button>
{
          currentStage == listHeader[listHeader.length - 1] && (
<button 
          onClick={handleDownload} 
          className={`bg-[#1F2937] text-white p-3 px-5 rounded-full ${!state.downloadEnable && llmGenerated && 'opacity-50 cursor-not-allowed'}`}
          disabled={!state.downloadEnabled && llmGenerated}>
            Download Document&nbsp;&nbsp;<DownloadIcon />
        </button>          )
        }
          </div>
      </div>
    </>
  );
}

export default Home;
