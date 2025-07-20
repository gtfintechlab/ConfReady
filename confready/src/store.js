import React, { createContext, useReducer, useContext, useEffect } from 'react';

const StoreContext = createContext();

// ========== HARDCODED DATA ==========

const HARDCODED_CHECKLISTS = {
  aclchecklist: [
    {
      "id": "A",
      "quest": {
        "section": "A",
        "questions": {
          "A1": "Did you discuss the limitations of your work?",
          "A2": "Did you discuss any potential risks of your work?",
          "A3": "Do the abstract and introduction summarize the paper’s main claims?"
        },
        "title": "For every submission",
        "titleResponse": 0,
        "numOfQuestions": 3
      }
    },
    {
      "id": "B",
      "quest": {
        "questions": {
          "B2": "Did you discuss the license or terms for use and/or distribution of any artifacts?",
          "B1": "Did you cite the creators of artifacts you used?",
          "B6": "Did you report relevant statistics like the number of examples, details of train/test/dev splits, etc. for the data that you used/created?",
          "B5": "Did you provide documentation of the artifacts, e.g., coverage of domains, languages, and linguistic phenomena, demographic groups represented, etc.?",
          "B4": "Did you discuss the steps taken to check whether the data that was collected/used contains any information that names or uniquely identifies individual people or offensive content, and the steps taken to protect / anonymize it?",
          "B3": "Did you discuss if your use of existing artifact(s) was consistent with their intended use, provided that it was specified? For the artifacts you create, do you specify intended use and whether that is compatible with the original access conditions (in particular, derivatives of data accessed for research purposes should not be used outside of research contexts)?"
        },
        "numOfQuestions": 6,
        "section": "B",
        "titleResponse": 1,
        "title": "Did you use or create scientific artifacts?"
      }
    },
    {
      "id": "C",
      "quest": {
        "questions": {
          "C2": "Did you discuss the experimental setup, including hyperparameter search and best-found hyperparameter values?",
          "C4": "If you used existing packages (e.g., for preprocessing, for normalization, or for evaluation), did you report the implementation, model, and parameter settings used (e.g., NLTK, Spacy, ROUGE, etc.)?",
          "C3": "Did you report descriptive statistics about your results (e.g., error bars around results, summary statistics from sets of experiments), and is it transparent whether you are reporting the max, mean, etc. or just a single run?",
          "C1": "Did you report the number of parameters in the models used, the total computational budget (e.g., GPU hours), and computing infrastructure used?"
        },
        "numOfQuestions": 4,
        "titleResponse": 1,
        "section": "C",
        "title": "Did you run computational experiments?"
      }
    },
    {
      "id": "D",
      "quest": {
        "section": "D",
        "titleResponse": 1,
        "title": "Did you use human annotators (e.g., crowdworkers) or research with human subjects?",
        "numOfQuestions": 5,
        "questions": {
          "D1": "Did you report the full text of instructions given to participants, including e.g., screenshots, disclaimers of any risks to participants or annotators, etc.?",
          "D5": "Did you report the basic demographic and geographic characteristics of the annotator population that is the source of the data?",
          "D3": "Did you discuss whether and how consent was obtained from people whose data you’re using/curating (e.g., did your instructions explain how the data would be used)?",
          "D4": "Was the data collection protocol approved (or determined exempt) by an ethics review board?",
          "D2": "Did you report information about how you recruited (e.g., crowdsourcing platform, students) and paid participants, and discuss if such payment is adequate given the participants’ demographic (e.g., country of residence)?"
        }
      }
    },
    {
      "id": "E",
      "quest": {
        "questions": {
          "E1": "Did you include information about your use of AI assistants?"
        },
        "section": "E",
        "titleResponse": 1,
        "title": "Did you use AI assistants (e.g., ChatGPT, Copilot) in your research, coding, or writing?",
        "numOfQuestions": 1
      }
    }],
  'neurips-checklist-a': [
    {
      "id": "1",
      "quest": {
        "titleResponse": 0,
        "section": "1",
        "title": "Claims",
        "questions": {
          "1.": "Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?"
        },
        "numOfQuestions": 1
      }
    },
    {
      "id": "10",
      "quest": {
        "title": "Broader Impacts",
        "questions": {
          "10. ": "Does the paper discuss both potential positive societal impacts and negative\nsocietal impacts of the work performed?"
        },
        "titleResponse": 0,
        "numberOfQuestions": 1,
        "section": "10"
      }
    },
    {
      "id": "11",
      "quest": {
        "section": "11",
        "numberOfQuestions": 1,
        "questions": {
          "11. ": "Does the paper describe safeguards that have been put in place for responsible\nrelease of data or models that have a high risk for misuse (e.g., pretrained language models,\nimage generators, or scraped datasets)?"
        },
        "titleResponse": 0,
        "title": "Safeguards"
      }
    },
    {
      "id": "12",
      "quest": {
        "section": "12",
        "questions": {
          "12. ": "Are the creators or original owners of assets (e.g., code, data, models), used in\nthe paper, properly credited and are the license and terms of use explicitly mentioned and\nproperly respected?"
        },
        "numberOfQuestions": 1,
        "title": "Licences for Existing Assets",
        "titleResponse": 0
      }
    },
    {
      "id": "13",
      "quest": {
        "titleResponse": 0,
        "title": "New Assets",
        "questions": {
          "13. ": "Are new assets introduced in the paper well documented and is the documentation\nprovided alongside the assets?"
        },
        "numberOfQuestions": 1,
        "section": "13"
      }
    },
    {
      "id": "14",
      "quest": {
        "numberOfQuestions": 1,
        "questions": {
          "14. ": "For crowdsourcing experiments and research with human subjects, does the paper\ninclude the full text of instructions given to participants and screenshots, if applicable, as\nwell as details about compensation (if any)?"
        },
        "section": "14",
        "titleResponse": 0,
        "title": "Crowdsourcing and Research with Human Subjects"
      }
    },
    {
      "id": "15",
      "quest": {
        "numberOfQuestions": 1,
        "questions": {
          "15. ": "Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained?"
        },
        "title": "Institutional Review Board (IRB) Approvals or Equivalent for Research with Human\nSubjects",
        "titleResponse": 0,
        "section": "15"
      }
    },
    {
      "id": "2",
      "quest": {
        "section": "2",
        "questions": {
          "2. ": "Does the paper discuss the limitations of the work performed by the authors?"
        },
        "title": "Limitations",
        "titleResponse": 0,
        "numOfQuestions": 1
      }
    },
    {
      "id": "3",
      "quest": {
        "title": "Theory Assumptions and Proofs",
        "questions": {
          "3.": "For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof?"
        },
        "titleResponse": 0,
        "numOfQuestions": 1,
        "section": "3"
      }
    },
    {
      "id": "4",
      "quest": {
        "title": "Experimental Result Reproducibility",
        "section": "4",
        "titleResponse": 0,
        "numOfQuestions": 1,
        "questions": {
          "4.": "Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)?"
        }
      }
    },
    {
      "id": "5",
      "quest": {
        "section": "5",
        "questions": {
          "5. ": "Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental\nmaterial?"
        },
        "numOfQuestions": 1,
        "titleResponse": 0,
        "title": "Open access to data and code"
      }
    },
    {
      "id": "6",
      "quest": {
        "section": "6",
        "titleResponse": 0,
        "title": "Experimental Setting/Details",
        "numOfQuestions": 1,
        "questions": {
          "6. ": "Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results?"
        }
      }
    },
    {
      "id": "7",
      "quest": {
        "title": "Experimental Statistical Significance",
        "titleResponse": 0,
        "section": "7",
        "questions": {
          "7.": "Does the paper report error bars suitably and correctly defined or other appropriate\ninformation about the statistical significance of the experiments?"
        },
        "numOfQuestions": 1
      }
    },
    {
      "id": "8",
      "quest": {
        "section": "8",
        "title": "Experiments Compute Resources",
        "titleResponse": 0,
        "numberOfQuestions": 1,
        "questions": {
          "8. ": "For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce\nthe experiments?"
        }
      }
    },
    {
      "id": "9",
      "quest": {
        "titleResponse": 0,
        "numberOfQuestions": 1,
        "questions": {
          "9. ": "Does the research conducted in the paper conform, in every respect, with the\nNeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?"
        },
        "title": "Code of Ethics",
        "section": "9"
      }
    }
  ],
  'neurips-checklist-b': [
    {
      "id": "1",
      "quest": {
        "questions": {
          "1. (b)": "Did you describe the limitations of your work?",
          "1. (c)": "Did you discuss any potential negative societal impacts of your work?",
          "1. (a)": "Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?",
          "1. (d)": "Have you read the ethics review guidelines and ensured that your paper conforms to them?"
        },
        "numOfQuestions": 4,
        "titleResponse": 0,
        "title": "For all authors ... ",
        "section": "1"
      }
    },
    {
      "id": "2",
      "quest": {
        "titleResponse": 0,
        "title": "If you are including theoretical results ...",
        "questions": {
          "2. (a)": "Did you state the full set of assumptions of all theoretical results?",
          "2. (b)": "Did you include complete proofs of all theoretical results?"
        },
        "numOfQuestions": 2,
        "section": "2"
      }
    },
    {
      "id": "3",
      "quest": {
        "titleResponse": 0,
        "section": "3",
        "numOfQuestions": 4,
        "questions": {
          "3. (d)": "Did you include the total amount of compute and the type of resources used (e.g., type of GPUs, internal cluster, or cloud provider)?",
          "3. (c)": "Did you report error bars (e.g., with respect to the random seed after running experiments multiple times)?",
          "3. (b)": "Did you specify all the training details (e.g., data splits, hyperparameters, how they were chosen)?",
          "3. (a)": "Did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)?"
        },
        "title": "If you ran experiments (e.g. for benchmarks) ..."
      }
    },
    {
      "id": "4",
      "quest": {
        "title": "If you are using existing assets (e.g. code, data, models) or curating/releasing new assets ...",
        "numberOfQuestions": 5,
        "section": "4",
        "titleResponse": 0,
        "questions": {
          "4. (d)": "Did you discuss whether and how consent was obtained from people whose data you’re using/curating?",
          "4. (c)": "Did you include any new assets either in the supplemental material or as a URL?",
          "4. (e)": "Did you discuss whether the data you are using/curating contains personally identifiable information or offensive content?",
          "4. (b)": "Did you mention the license of the assets?",
          "4. (a)": "If your work uses existing assets, did you cite the creators?"
        }
      }
    },
    {
      "id": "5",
      "quest": {
        "questions": {
          "5. (a)": "Did you include the full text of instructions given to participants and screenshots, if applicable?",
          "5. (b)": "Did you describe any potential participant risks, with links to Institutional Review Board (IRB) approvals, if applicable?",
          "5. (c)": "Did you include the estimated hourly wage paid to participants and the total amount spent on participant compensation?"
        },
        "titleResponse": 0,
        "numberOfQuestions": 3,
        "title": "If you used crowdsourcing or conducted research with human subjects ... ",
        "section": "5"
      }
    }
  ],
};

// ========== END HARDCODED DATA ==========

const initialState = {
  confQuestions: [],
  currentStage: 'A',
  responses: {},
  sectionProgress: {},
  user: null,
  timeTaken: '',
  issues: {},
  checklistName: 'aclchecklist', // or 'neurips-checklist-a', etc.
  llmGenerated: 0,
  bottomReached: { 'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0 },
  downloadEnabled: 0,
  sidebarStage: 1,
};

const calculateProgress = (responses, questions) => {
  const progress = {};
  questions.forEach(section => {
    const sectionId = section.id;
    const numOfQuestions = section.quest.numOfQuestions || section.quest.numberOfQuestions;
    progress[sectionId] = { total: numOfQuestions, answered: 0 };
  });
  for (const key in responses) {
    for (const section of questions) {
      const questionIds = Object.keys(section.quest.questions);
      if (questionIds.includes(key) && responses[key].text) {
        progress[section.id].answered += 1;
      }
    }
  }
  for (const section in progress) {
    progress[section] = (progress[section].answered / progress[section].total) * 100;
  }
  return progress;
};

const reducer = (state, action) => {
  switch (action.type) {
    case 'SET_QUESTIONS':
      const initialResponses = action.payload.reduce((acc, section) => {
        const questionIds = Object.keys(section.quest.questions);
        questionIds.forEach((qid) => {
          acc[qid] = { choice: true, text: '' };
        });
        return acc;
      }, {});
      return {
        ...state,
        confQuestions: action.payload,
        responses: initialResponses,
      };
    case 'SET_ISSUES':
      return { ...state, issues: action.payload };
    case 'SET_CURRENT_STAGE':
      return { ...state, currentStage: action.payload };
    case 'SET_TIME':
      return { ...state, timeTaken: action.payload };
    case 'SET_RESPONSE':
      const updatedResponses = {
        ...state.responses,
        [action.payload.id]: action.payload.response,
      };
      const updatedProgress = calculateProgress(updatedResponses, state.confQuestions);
      return {
        ...state,
        responses: updatedResponses,
        sectionProgress: updatedProgress,
      };
    case 'RESET_RESPONSE':
      const resetResponses = Object.keys(state.responses).reduce((acc, key) => {
        acc[key] = { choice: true, text: '' };
        return acc;
      }, {});
      return { ...state, responses: resetResponses };
    case 'RESET_PROGRESS':
      return { ...state, sectionProgress: {} };
    case 'RESET_BOTTOM_REACHED':
      return { ...state, bottomReached: {} };
    case 'SET_BOTTOM_REACHED':
      const newBottomReached = { ...state.bottomReached, [action.payload.section]: action.payload.value };
      const downloadEnabled = Object.values(newBottomReached).every(value => value === 1) ? 1 : 0;
      return { ...state, bottomReached: newBottomReached, downloadEnabled };
    case 'SET_BOTTOM_INITIAL_STATE':
      return { ...state, bottomReached: action.payload };
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_CHECKLIST':
      return { ...state, checklistName: action.payload };
    case 'SET_LLM_GENERATION':
      return { ...state, llmGenerated: action.payload };
    case 'SET_SIDEBAR_STAGE':
      return { ...state, sidebarStage: action.payload };
    default:
      return state;
  }
};

export const StoreProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    // Set questions from the selected hardcoded checklist
    const questions = HARDCODED_CHECKLISTS[state.checklistName] || [];
    if (questions.length === 0) {
      console.warn('No hardcoded questions data found for', state.checklistName);
    }
    dispatch({ type: 'SET_QUESTIONS', payload: questions });
  }, [state.checklistName]);

  return (
    <StoreContext.Provider value={{ state, dispatch }}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => useContext(StoreContext);
