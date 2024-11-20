import React, { useState, useRef, useEffect } from 'react';
import aclLogo from '../../assets/aclready.png';
import AuthModal from '../AuthModal/AuthModal';
import { useStore } from '../../store';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { useDropzone } from 'react-dropzone';
import { useTheme } from '@mui/material/styles';
import GitHubIcon from '@mui/icons-material/GitHub';
import Person2Icon from '@mui/icons-material/Person2';
import ClassIcon from '@mui/icons-material/Class';
import ModeNightIcon from '@mui/icons-material/ModeNight';

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const checklists = [
  'Association for Computational Linguistics (ACL)',
  'NeurIPS',
];

function getStyles(name, checklistName, theme) {
  return {
    fontWeight: checklistName.includes(name)
      ? theme.typography.fontWeightMedium
      : theme.typography.fontWeightRegular,
  };
}

export default function Sidebar() {
  const [open, setOpen] = useState(false);
  const { state, dispatch } = useStore();
  const hiddenFileInput = useRef(null);
  const [loadingFile, setLoadingFile] = useState(false);
  const [jsonContent, setJsonContent] = useState(null);
  const [loadingStage, setLoadingStage] = useState("");
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: (acceptedFiles) => {
      handleFileChangeDrop(acceptedFiles);
    },
  });

  const theme = useTheme();
  const [checklistName, setChecklistName] = useState([]);

  const handleClick = () => {
    hiddenFileInput.current.click();
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      dispatch({ type: 'SET_ISSUES', payload: {} });
      dispatch({ type: 'SET_CURRENT_STAGE', payload: 'A' });
      dispatch({ type: 'SET_TIME', payload: '' });
      dispatch({ type: 'RESET_RESPONSE' });
      dispatch({ type: 'RESET_PROGRESS' });
      setLoadingStage("Loading...");

      const eventSource = new EventSource('http://localhost:8080/api/upload/status');

      eventSource.onmessage = function (event) {
        setLoadingStage(event.data);
      };

      const response = await fetch('http://localhost:8080/api/upload', {
        method: 'POST',
        body: formData,
      });

      eventSource.close();

      const result = await response.json();
      if (result.error) {
        alert(result.error);
      } else {
        setJsonContent(result);
        console.log(result);
        dispatch({ type: 'SET_TIME', payload: result['time_taken'] });
        dispatch({ type: 'SET_ISSUES', payload: result['issues'] });
        for (const key in result) {
          let section_name = result[key]['section name'];
          dispatch({
            type: 'SET_RESPONSE',
            payload: {
              id: key,
              response: {
                choice: section_name === 'None' ? false : true,
                text: section_name + ". " + result[key]['justification'],
                s_name: section_name,
              },
            },
          });
        }
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoadingFile(false);
      dispatch({type: 'SET_LLM_GENERATION', payload: 1});
      dispatch({type: 'RESET_BOTTOM_REACHED'});
    }
  };

  const handleChange = async (event) => {
    const fileUploaded = event.target.files[0];
    let file_size = fileUploaded.size;

    setLoadingFile(true);

    if (file_size > 10000000) {
      alert("File size should not exceed 10MB.");
      setLoadingFile(false);
      return;
    }

    await handleFileUpload(fileUploaded);
  };

  const handleFileChangeDrop = async (filesAccepted) => {
    const fileUploaded = filesAccepted[0];
    let file_size = fileUploaded.size;

    setLoadingFile(true);

    if (file_size > 5000000) {
      alert("File size should not exceed 5MB.");
      setLoadingFile(false);
      return;
    }

    await handleFileUpload(fileUploaded);
  };

  useEffect(() => {
    // This useEffect can be used to set any initial state if needed
  }, []);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange2 = (value) => {
  
    // Directly set checklist name value
    const selectedChecklist = value;
  
    setChecklistName(selectedChecklist);
  
    if (selectedChecklist === 'Association for Computational Linguistics (ACL)') {
      dispatch({ type: 'SET_CHECKLIST', payload: 'aclchecklist' });
      dispatch({type: 'SET_CURRENT_STAGE', payload: 'A'});
      dispatch({type: 'RESET_PROGRESS'})
      dispatch({type: 'SET_LLM_GENERATION', payload: 0});
      dispatch({type: 'RESET_BOTTOM_REACHED'});
      dispatch({type: 'SET_BOTTOM_INITIAL_STATE', payload: {'A':0,  'B': 0, 'C': 0, 'D': 0, 'E': 0}});
    } else if (selectedChecklist === 'NeurIPS') {
      dispatch({ type: 'SET_CHECKLIST', payload: 'neurips-checklist-a' });
      dispatch({type: 'SET_CURRENT_STAGE', payload: '1'});
      dispatch({type: 'RESET_PROGRESS'})
      dispatch({type: 'SET_LLM_GENERATION', payload: 0});
      dispatch({type: 'RESET_BOTTOM_REACHED'});
      dispatch({type: 'SET_BOTTOM_INITIAL_STATE', payload: {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}});
    }
  };

  // Function to validate file types
const validateFileType = (e) => {
  const file = e.target.files[0];
  if (!file) return;

  // Allowed file extensions
  const allowedExtensions = ['.tex', '.zip', '.tar.gz'];
  const fileName = file.name.toLowerCase();

  // Check if the file extension is allowed
  if (allowedExtensions.some(ext => fileName.endsWith(ext))) {
    handleChange(e); // Call your existing handler if valid
  } else {
    alert('Invalid file type! Please upload a .tex, .zip, or .tar.gz file.');
    e.target.value = ''; // Clear the input
  }
};
  
return (
  <>
    <div
      className={`fixed w-full h-full bg-[rgba(0,0,0,0.7)] z-50 top-0 left-0 flex items-center justify-center ${
        loadingFile ? '' : 'hidden'
      } flex flex-col`}
    >
      <img
        id="loading-logo"
        className="h-40 rounded-full animate-pulse"
        src={aclLogo}
        alt="Logo"
      />
      <h1 className="text-white text-2xl m-6 animate-pulse">{loadingStage}</h1>
    </div>

    <AuthModal open={open} onClose={handleClose} />

    <aside
      id="logo-sidebar"
      style={{ borderTopRightRadius: 120 }}
      className="fixed top-0 left-0 z-40 w-72 h-screen pt-8 transition-transform -translate-x-full border-r sm:translate-x-0 bg-gray-800 border-gray-700 items-center flex flex-col justify-between"
      aria-label="Sidebar"
    >
      <div className="flex flex-col justify-center items-center">
        {/* Logo Section */}
        <div className="px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800 mt-4"> {/* Reduced spacing */}
          <img src={aclLogo} className="h-[120px]" alt="ACL Logo" />
        </div>
        <p className="text-white text-center px-8 lekton text-sm mt-2">
          {/* Minimized spacing */}
          AI powered solution for seamlessly filling out the ACL Responsible
          Checklist.
        </p>

        {/* New Icon Section */}
        <div className="flex flex-row mt-3 gap-4 justify-center">
          {/* Profile Icon */}
          <button
            className="bg-gray-700 hover:bg-gray-600 p-3 rounded-full transition-all duration-300 shadow-md text-white"
            title="Profile / Authentication"
          >
            <Person2Icon fontSize="medium" />
          </button>

          {/* Documentation Icon */}
          <button
            onClick={() =>
              window.open("https://confcheck-docs.vercel.app", "_blank")
            }
            className="bg-gray-700 hover:bg-gray-600 p-3 rounded-full transition-all duration-300 shadow-md text-white"
            title="Documentation"
          >
            <ClassIcon fontSize="medium" />
          </button>

          {/* GitHub Icon */}
          <button
            onClick={() =>
              window.open(
                "https://github.com/gtfintechlab/ACL_SystemDemonstrationChecklist",
                "_blank"
              )
            }
            className="bg-gray-700 hover:bg-gray-600 p-3 rounded-full transition-all duration-300 shadow-md text-white"
            title="GitHub Repository"
          >
            <GitHubIcon fontSize="medium" />
          </button>

          {/* Theme Toggle Icon */}
          <button
            className="bg-gray-700 hover:bg-gray-600 p-3 rounded-full transition-all duration-300 shadow-md text-white"
            title="Toggle Dark / Light Mode"
          >
            <ModeNightIcon fontSize="medium" />
          </button>
        </div>

        {/* Checklist Dropdown */}
        <div className="w-full px-4 mt-3">
          <label
            htmlFor="checklist-dropdown"
            className="block text-sm font-medium text-gray-300 lekton mb-2"
          >
            Checklist
          </label>
          <div className="relative">
            <select
              id="checklist-dropdown"
              value={checklistName}
              onChange={(e) => handleChange2(e.target.value)}
              className="block w-full bg-[#314869] text-white rounded-md px-6 py-3 border-none shadow-md focus:ring-2 focus:ring-blue-500 transition-all duration-300 truncate appearance-none"
              style={{ outline: "none", cursor: "pointer" }}
            >
              {checklists.map((name) => (
                <option
                  key={name}
                  value={name}
                  className="truncate text-black bg-white hover:bg-gray-200 transition-all duration-300 rounded-md"
                >
                  {name}
                </option>
              ))}
            </select>
            <span className="absolute inset-y-0 right-6 flex items-center pointer-events-none text-gray-400">
              ▼
            </span>
          </div>
        </div>

        {/* New LLM Dropdown */}
        <div className="w-full px-4 mt-4">
          <label
            htmlFor="llm-dropdown"
            className="block text-sm font-medium text-gray-300 lekton mb-2"
          >
            Large Language Model (LLM)
          </label>
          <div className="relative">
            <select
              id="llm-dropdown"
              className="block w-full bg-[#314869] text-white rounded-md px-6 py-3 border-none shadow-md focus:ring-2 focus:ring-blue-500 transition-all duration-300 truncate appearance-none"
              style={{ outline: "none", cursor: "pointer" }}
            >
              <option
                value="chatgpt-4"
                className="truncate text-black bg-white hover:bg-gray-200 transition-all duration-300 rounded-md"
              >
                ChatGPT-4
              </option>
              <option
                value="4o"
                className="truncate text-black bg-white hover:bg-gray-200 transition-all duration-300 rounded-md"
              >
                4o
              </option>
              <option
                value="o1-preview"
                className="truncate text-black bg-white hover:bg-gray-200 transition-all duration-300 rounded-md"
              >
                o1-preview
              </option>
            </select>
            <span className="absolute inset-y-0 right-6 flex items-center pointer-events-none text-gray-400">
              ▼
            </span>
          </div>
        </div>
      </div>

      {/* Upload Document Section */}
      <div
        className="w-full px-4 py-3 bg-[#003057] border-t-2 border-gray-700 flex flex-col items-center mt-6 mb-6"
      >
        <h1 className="text-white font-bold text-base mb-4">Upload Document</h1>

        <div
          {...getRootProps()}
          onClick={() => handleClick()}
          className="cursor-pointer border-dotted py-20 rounded-md border-2 border-white w-64 flex flex-col items-center"
        >
          <input
            {...getInputProps()}
            type="file"
            accept=".tex,.zip,.tar.gz"
            onChange={handleChange}
            ref={hiddenFileInput}
            style={{ display: "none" }}
          />
          {loadingFile ? (
            <div className="container flex justify-center mb-7">
              <div className="loader">
                <div></div>
                <div></div>
                <div></div>
              </div>
            </div>
          ) : (
            <AddCircleIcon className="text-white" fontSize="large" />
          )}
          <p className="text-white text-center lekton text-sm mt-6">
            {!loadingFile
              ? "Upload or drag and drop your file here"
              : "Please Wait..."}
          </p>
        </div>
      </div>
    </aside>
  </>
);


}
