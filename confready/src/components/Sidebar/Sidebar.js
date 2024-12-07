import React, { useState, useRef, useEffect } from 'react';
import confReadyLogo from '../../assets/confready.png';
import AuthModal from '../AuthModal/AuthModal';
import { useStore } from '../../store';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { useDropzone } from 'react-dropzone';
import { useTheme } from '@mui/material/styles';
import GitHubIcon from '@mui/icons-material/GitHub';
import ClassIcon from '@mui/icons-material/Class';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import { saveAs } from 'file-saver';

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
  'ACL',
  'NeurIPS',
  'NeurIPS D&B',
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
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [llm, setLlm] = useState('Llama 3.1 405B')

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const theme = useTheme();
  const [checklistName, setChecklistName] = useState([]);

  const handleClick = () => {
    dispatch({type: 'SET_SIDEBAR_STAGE', payload: 2});
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
      dispatch({type: 'SET_SIDEBAR_STAGE', payload: 3});
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
    } else if(selectedChecklist === 'NeurIPS Datasets and Benchmarks') {
      dispatch({ type: 'SET_CHECKLIST', payload: 'neurips-checklist-b' });
      dispatch({type: 'SET_CURRENT_STAGE', payload: '1'});
      dispatch({type: 'RESET_PROGRESS'})
      dispatch({type: 'SET_LLM_GENERATION', payload: 0});
      dispatch({type: 'RESET_BOTTOM_REACHED'});
      dispatch({type: 'SET_BOTTOM_INITIAL_STATE', payload: {'1': 0, '2': 0,}});
    }
  };

  const generateMarkdown = () => {
    let markdown = "# ACL Responsible Checklist Responses\n\n";
    if(state.timeTaken) {
      markdown += `${state.timeTaken}\n\n`
    }

    state.confQuestions.forEach(({ id, quest }) => {
      markdown += `## Section ${id}: ${quest.title}\n\n`;

      Object.keys(quest.questions).sort((a, b) => {
        const numA = parseInt(a.slice(1), 10);
        const numB = parseInt(b.slice(1), 10);
        return numA - numB;
      }).forEach(questionId => {
        const questionText = quest.questions[questionId];
        const response = state.responses[questionId];

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
      dispatch({ type: 'SET_BOTTOM_REACHED', payload: { section: state.currentStage, value: 1 } });
    }
  };
  
return (
  <>
    <div
      className={`fixed w-full h-full bg-[rgba(0,0,0,0.7)] z-50 top-0 left-0 flex items-center justify-center ${
        loadingFile ? '' : 'hidden'
      } flex-col`}
    >
      <img
        id="loading-logo"
        className="h-24 rounded-full animate-pulse"
        src={confReadyLogo}
        alt="Logo"
      />
      <h1 className="text-white text-2xl m-6 animate-pulse">{loadingStage}</h1>
    </div>

    <AuthModal open={open} onClose={handleClose} />

    <aside
      id="logo-sidebar"
      style={{ borderTopRightRadius: 30 }}
      className="fixed top-0 left-0 z-40 w-72 h-screen pt-8 transition-transform -translate-x-full border-r sm:translate-x-0 bg-gray-800 border-gray-700 items-center flex flex-col justify-between"
      aria-label="Sidebar"
    >
      <div className="flex flex-col justify-between h-full w-full">
        {/* Logo Section */}
        <div className="flex flex-col justify-center items-center">
          <div className="px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800 mt-4"> {/* Reduced spacing */}
            <img src={confReadyLogo} className="h-[75px]" alt="ACL Logo" />
          </div>
          <p className="text-white text-center px-8 lekton text-sm mt-4">
            {/* Minimized spacing */}
            AI powered solution for seamlessly filling out various conference checklists
          </p>
        </div>

      {/* Upload Document Section */}
      <div className="w-full px-4 py-3 bg-[#003057] flex flex-col mt-3 rounded-3xl justify-between flex-grow">
  <div className="flex flex-col flex-grow">
    {/* Checklist Dropdown */}
    <div className="w-full px-4 mt-3">
      <label
        htmlFor="checklist-dropdown"
        className="block text-sm font-medium text-gray-300 lekton mb-3"
      >
        <button onClick={() => {
          dispatch({type: 'SET_SIDEBAR_STAGE', payload: 1});
          const dropdown = document.getElementById("checklist-dropdown");
          dropdown.click(); 
        }} className={`${state.sidebarStage == 1 ? 'bg-white text-[#003057] px-1 py-1 w-7' : 'border-dotted border-gray-400 border-2 text-white px-1 py-1 w-8'} rounded-full`}>
          1
        </button>{" "}
        Select Conference
      </label>
      <div className="relative mb-2">
        <select
          id="checklist-dropdown"
          value={checklistName}
          onChange={(e) => handleChange2(e.target.value)}
          className="text-sm block w-full bg-[#314869] text-gray-200 rounded-md px-4 py-2 border-none shadow-md transition-all duration-300 truncate appearance-none"
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
        <span className="absolute inset-y-0 right-6 flex items-center pointer-events-none text-[#003057]">
          ▼
        </span>
      </div>
    </div>
    <div className='px-4'>
      <label
        htmlFor="checklist-dropdown"
        className="block text-sm font-medium text-gray-300 lekton py-3"
      >
        <button onClick={() => {
          dispatch({type: 'SET_SIDEBAR_STAGE', payload: 2});
          handleClick();
        }} className={`${state.sidebarStage == 2 ? 'bg-white text-[#003057] px-1 py-1 w-7' : 'border-dotted border-gray-400 border-2 text-white px-1 py-1 w-8'} rounded-full text-sm items-center justify-center`}>
          2
        </button>{" "}
        Upload Document
      </label>

      <div
        {...getRootProps()}
        onClick={() => handleClick()}
        className="cursor-pointer bg-[#314869] py-3 rounded-md flex flex-col items-center"
      >
        <input
          {...getInputProps()}
          type="file"
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
          <div className="border-2 border-dashed border-gray-400 px-3 py-4">
            <AddCircleIcon className="text-white" fontSize="medium" />
          </div>
        )}
        <p className="text-white text-center lekton text-sm mt-3">
          {!loadingFile
            ? "Upload or drag and drop your file here"
            : "Please Wait..."}
        </p>
      </div>

      <label
        htmlFor="checklist-dropdown"
        className="block text-sm font-medium text-gray-300 lekton py-3"
      >
        <button onClick={() => {
          if(state.llmGenerated != 1) {
            window.alert("Please upload .tex or .tar.gz file in step 2");
          } else {
            dispatch({type: 'SET_SIDEBAR_STAGE', payload: 3});
          }
        }} className={`${state.sidebarStage == 3 ? 'bg-white text-[#003057] px-1 py-1 w-7' : 'border-dotted border-gray-400 border-2 text-white px-1 py-1 w-8'} rounded-full text-sm`}>
          3
        </button>{" "}
        Review/Edit
      </label>

      <label
        htmlFor="checklist-dropdown"
        className="block text-sm font-medium text-gray-300 lekton py-3"
      >
        <button onClick={() => {
          if(state.downloadEnabled == 1) {
            dispatch({type: 'SET_SIDEBAR_STAGE', payload: 4});
            handleDownload();
          }
        }} className={`${state.sidebarStage == 4 ? 'bg-white text-[#003057] px-1 py-1 w-7' : 'border-dotted border-gray-400 border-2 text-white px-1 py-1 w-8'} rounded-full text-sm`}>
          4
        </button>{" "}
        Download
      </label>
    </div>
  </div>
          {/* New Icon Section */}
          {/* Language Model Icon */}
          <div className="flex flex-row items-center relative space-x-2">
  {/* Icon Button */}
  <button
    className="bg-gray-700 hover:bg-gray-600 rounded-full transition-all duration-300 shadow-md text-white w-fit"
    title="Language Model"
    style={{paddingLeft: 10, paddingRight: 10, paddingTop: 6, paddingBottom: 6}}
  >
    <AutoAwesomeIcon sx={{ fontSize: 16 }} />
  </button>

  {/* Selected Model and Dropdown in one line */}
  <div className="flex flex-row items-center text-sm text-gray-200 truncate">
    <p className="mr-2 whitespace-nowrap">Selected Model:</p>
    <button
      className="bg-gray-700 text-sm hover:bg-gray-600 px-2 py-1 rounded-md transition-all duration-300 text-white truncate"
      onClick={toggleDropdown}
      title="Options"
    >
      {llm}
    </button>
  </div>

  {/* Dropdown Menu */}
  {isDropdownOpen && (
          <div className="absolute bottom-12 bg-[#314869] text-white rounded-md shadow-md px-4 py-2 w-52 z-50">
            <p className="text-sm font-medium text-gray-300 lekton mb-2">
              Select Language Model
            </p>
      <ul className="space-y-2">
        <li
          className="cursor-pointer hover:bg-gray-600 px-3 py-2 rounded-md text-sm"
          onClick={() => {
            setLlm("Llama 3.1 405B");
            toggleDropdown();
          }}
        >
          Llama 3.1 405B
        </li>
        <li
          className="cursor-pointer hover:bg-gray-600 px-3 py-2 rounded-md text-sm"
          onClick={() => {
            setLlm("4o");
            toggleDropdown();
          }}
        >
          4o
        </li>
        <li
          className="cursor-pointer hover:bg-gray-600 px-3 py-2 rounded-md text-sm"
          onClick={() => {
            setLlm("o1-preview");
            toggleDropdown();
          }}
        >
          o1-preview
        </li>
      </ul>
    </div>
  )}
</div>

    
<div className="flex flex-col mt-3 gap-2 justify-center">
  {/* Documentation Icon */}
  <div className='flex flex-row items-center'>
  <button
    onClick={() =>
      window.open("https://confready-docs.vercel.app", "_blank")
    }
    className="bg-gray-700 hover:bg-gray-600 rounded-full transition-all duration-300 shadow-md text-white w-fit"
    title="Documentation"
    style={{paddingLeft: 10, paddingRight: 10, paddingTop: 6, paddingBottom: 6}}
  >
    <ClassIcon sx={{ fontSize: 16 }} />
  </button>
  <p className='text-gray-200 ml-2 text-sm'>Documentation</p>
  </div>

  {/* GitHub Icon */}
  <div className='flex flex-row items-center'>
  <button
    onClick={() =>
      window.open(
        "https://github.com/gtfintechlab/ACL_SystemDemonstrationChecklist",
        "_blank"
      )
    }
    className="bg-gray-700 hover:bg-gray-600 rounded-full transition-all duration-300 shadow-md text-white w-fit"
    title="GitHub Repository"
    style={{paddingLeft: 10, paddingRight: 10, paddingTop: 6, paddingBottom: 6}}
  >
    <GitHubIcon sx={{ fontSize: 16 }} />
  </button>
  <p className='text-gray-200 ml-2 text-sm'>GitHub</p>
  </div>

</div>
</div>

      </div>
    </aside>
  </>
);


}
