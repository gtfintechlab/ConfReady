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

  const handleChange = async (event) => {
    const fileUploaded = event.target.files[0];
    let file_size = fileUploaded.size;

    setLoadingFile(true);

    if (file_size > 5000000) {
      alert("File size should not exceed 5MB.");
      setLoadingFile(false);
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      const data = JSON.parse(content);
      setJsonContent(data);

      for (const key in data) {
        dispatch({
          type: 'SET_RESPONSE',
          payload: {
            id: key,
            response: {
              choice: true,
              text: data[key]['justification']
            }
          }
        });
      }

      setLoadingFile(false);
    };
    reader.readAsText(fileUploaded);
  };

  useEffect(() => {
    const data = require('./sample_output.json');
    setJsonContent(data);
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

      {/* <nav className="fixed top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
        <div className="px-3 py-3 lg:px-5 lg:pl-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center justify-start rtl:justify-end">
              <button
                data-drawer-target="logo-sidebar"
                data-drawer-toggle="logo-sidebar"
                aria-controls="logo-sidebar"
                type="button"
                className="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
              >
                <span className="sr-only">Open sidebar</span>
                <svg
                  className="w-6 h-6"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    clipRule="evenodd"
                    fillRule="evenodd"
                    d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
                  ></path>
                </svg>
              </button>
              <a href="https://gatech.edu" className="flex ms-2 md:me-24">
                <img
                  src="https://www.gatech.edu/themes/contrib/gt_theme/images/gt-logo-oneline-white.svg"
                  className="h-8 me-3"
                />
              </a>
            </div>
            <div className="flex items-center">
              <div className="flex items-center ms-3">
                <div>
                  {!user ? (
                    <button
                      type="button"
                      className="flex text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600"
                      aria-expanded="false"
                      data-dropdown-toggle="dropdown-user"
                    >
                      <span className="sr-only">Open user menu</span>
                      <h1 onClick={handleClickOpen} className="text-white font-semibold">
                        LOG IN
                      </h1>
                    </button>
                  ) : (
                    <div className="flex items-center" onClick={() => {
                      let text;
if (window.confirm("Do you want to logout ?") == true) {
  auth.signOut();
}
                    }}>
                      <img
                        src={user.photoURL ? user.photoURL : "https://static.vecteezy.com/system/resources/thumbnails/001/840/618/small/picture-profile-icon-male-icon-human-or-people-sign-and-symbol-free-vector.jpg"}
                        alt="User Profile"
                        className="w-10 h-10 rounded-full cursor-pointer"
                      />
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </nav> */}

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
          <aside
        style={{borderTopRightRadius: 120}}
        className="z-40 w-72 h-screen mt-10 transition-transform -translate-x-full border-r sm:translate-x-0 bg-[#003057] border-[#003057] items-center flex flex-col"
      >
        <h1 className='text-white font-bold text-base mt-12'>Upload Document</h1>
        <input
        type="file"
        // accept=".tex"
        onChange={handleChange}
        ref={hiddenFileInput}
        style={{display: 'none'}}
      />
        <div onClick={() =>handleClick()} className='cursor-pointer border-dotted m-6 py-28 rounded-sm border-2 border-white w-fit flex flex-col items-center'>
        {loadingFile ? (
                  <div class="container flex justify-center mb-7"><div class="loader">
  <div></div>
  <div></div>
  <div></div>
</div></div>
                ):(
                  <AddCircleIcon className='text-white' fontSize="large" />
                )}
          <p className='text-white text-center'>Upload or drag and drop your file here</p>
        </div>
      </aside>
      </aside>
    </>
  );
}
