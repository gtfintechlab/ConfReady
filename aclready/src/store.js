import React, { createContext, useReducer, useContext, useEffect } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import db, { auth } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';

const StoreContext = createContext();

const initialState = {
  confQuestions: [],
  currentStage: 'A',
  responses: {},
  sectionProgress: {},
  user: null,
  timeTaken: '',
  issues: {},
  checklistName: 'aclchecklist',
  llmGenerated: 0,
  bottomReached: {'A':0,  'B': 0, 'C': 0, 'D': 0, 'E': 0},
  downloadEnabled: 0,
  sidebarStage: 1,
};

const calculateProgress = (responses, questions) => {
  const progress = {};
  questions.forEach(section => {
    const sectionId = section.id;
    const numOfQuestions = section.quest.numOfQuestions;
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
      return {
        ...state,
        issues: action.payload,
      };
    case 'SET_CURRENT_STAGE':
      return {
        ...state,
        currentStage: action.payload,
      };
    case 'SET_TIME':
      return {
        ...state,
        timeTaken: action.payload,
      };
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
      return {
        ...state,
        responses: resetResponses,
      };
    case 'RESET_PROGRESS':
      return {
        ...state,
        sectionProgress: {},
      };
    case 'RESET_BOTTOM_REACHED':
      return {
        ...state,
        bottomReached: {},
      };
    case 'SET_BOTTOM_REACHED':
      const newBottomReached = {...state.bottomReached, [action.payload.section]: action.payload.value};

      const downloadEnabled = Object.values(newBottomReached).every(value => value === 1) ? 1 : 0;
      return {
        ...state,
        bottomReached: newBottomReached,
        downloadEnabled: downloadEnabled,
      };
    case 'SET_BOTTOM_INITIAL_STATE':
      return {
        ...state,
        bottomReached: action.payload,
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
      };
    case 'SET_CHECKLIST':
      return {
        ...state,
        checklistName: action.payload,
      };
    case 'SET_LLM_GENERATION':
      return {
        ...state,
        llmGenerated: action.payload,
      };
    case 'SET_SIDEBAR_STAGE':
      return {
        ...state,
        sidebarStage: action.payload,
      };
    default:
      return state;
  }
};

export const StoreProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const querySnapshot = await getDocs(collection(db, state.checklistName));
        const questions = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          quest: doc.data(),
        }));
        if (questions.length === 0) {
          console.error('No questions found in the selected checklist.');
        } else {
          dispatch({ type: 'SET_QUESTIONS', payload: questions });
        }
      } catch (error) {
        console.error('Error fetching questions:', error);
      }
    };

    if (state.checklistName) {
      fetchData();
    }

    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if (user) {
        const userDetails = {
          uid: user.uid,
          email: user.email,
          displayName: user.displayName,
          photoURL: user.photoURL,
        };
        dispatch({ type: 'SET_USER', payload: userDetails });
      } else {
        dispatch({ type: 'SET_USER', payload: null });
      }
    });

    return () => unsubscribe();
  }, [state.checklistName]);

  return (
    <StoreContext.Provider value={{ state, dispatch }}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => useContext(StoreContext);
