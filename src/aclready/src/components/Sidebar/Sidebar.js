import React, { useState, useRef, useEffect } from 'react';
import aclLogo from '../../assets/aclready.png';
import AuthModal from '../AuthModal/AuthModal';
import { useStore } from '../../store';
import db, { auth } from '../../firebase';
import AddCircleIcon from '@mui/icons-material/AddCircle';

export default function Sidebar() {
  const [open, setOpen] = useState(false);
  const { state, dispatch } = useStore();
  const hiddenFileInput = useRef(null);
  const [loadingFile, setLoadingFile] = useState(false);
  const [jsonContent, setJsonContent] = useState(null);

  const handleClick = () => {
    hiddenFileInput.current.click();
  };

  const handleFileUpload = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Uploading file...');
      const response = await fetch('http://localhost:8080/api/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (result.error) {
        alert(result.error);
      } else {
        console.log('File processed successfully:', result);
        setJsonContent(result);
        for (const key in result) {
          dispatch({
            type: 'SET_RESPONSE',
            payload: {
              id: key,
              response: {
                choice: true,
                text: result[key]['justification'],
              },
            },
          });
        }
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoadingFile(false);
    }
  };

  const handleChange = async (event) => {
    const fileUploaded = event.target.files[0];
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

  return (
    <>
      <AuthModal open={open} onClose={handleClose} />

      <aside
        id="logo-sidebar"
        style={{borderTopRightRadius: 120}}
        className="fixed top-0 left-0 z-40 w-72 h-screen pt-10 transition-transform -translate-x-full border-r sm:translate-x-0 bg-gray-800 border-gray-700 items-center flex flex-col justify-between"
        aria-label="Sidebar"
      >
        <div className="flex flex-col mt-12 justify-center items-center">
          <div className="px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800">
            <img src={aclLogo} className="h-[150px]" />
          </div>
          <p className="text-white text-center">
            AI powered solution for seamlessly filling out the ACL Responsible Checklist.
          </p>
        </div>
        <div className="flex flex-col items-center mt-10">
          <h1 className='text-white font-bold text-base mt-12'>Upload Document</h1>
          <input
            type="file"
            onChange={handleChange}
            ref={hiddenFileInput}
            style={{display: 'none'}}
          />
          <div onClick={handleClick} className='cursor-pointer border-dotted m-6 py-28 rounded-sm border-2 border-white w-fit flex flex-col items-center'>
            {loadingFile ? (
              <div className="container flex justify-center mb-7">
                <div className="loader">
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
              </div>
            ) : (
              <AddCircleIcon className='text-white' fontSize="large" />
            )}
            <p className='text-white text-center'>Upload or drag and drop your file here</p>
          </div>
        </div>
      </aside>
    </>
  );
}
