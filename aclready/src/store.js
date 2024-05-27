import React, { createContext, useReducer, useContext, useEffect } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import db, { auth } from './firebase';
import { onAuthStateChanged } from 'firebase/auth';

const StoreContext = createContext();

const initialState = {
  aclQuestions: [],
  currentStage: 'A',
  responses: {},
  user: null,
};

const reducer = (state, action) => {
  switch (action.type) {
    case 'SET_QUESTIONS':
      return {
        ...state,
        aclQuestions: action.payload,
      };
    case 'SET_CURRENT_STAGE':
      return {
        ...state,
        currentStage: action.payload,
      };
    case 'SET_RESPONSE':
      return {
        ...state,
        responses: {
          ...state.responses,
          [action.payload.id]: action.payload.response,
        },
      };
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
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
        const querySnapshot = await getDocs(collection(db, 'aclchecklist'));
        const questions = querySnapshot.docs.map((doc) => ({
          id: doc.id,
          quest: doc.data(),
        }));
        dispatch({ type: 'SET_QUESTIONS', payload: questions });
      } catch (error) {
        console.error('Error fetching ACL questions:', error);
      }
    };

    fetchData();

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
  }, []);

  return (
    <StoreContext.Provider value={{ state, dispatch }}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => useContext(StoreContext);
