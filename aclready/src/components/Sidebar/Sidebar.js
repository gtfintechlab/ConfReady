import React, { useState } from 'react';
import aclLogo from '../../assets/aclready.png';
import AuthModal from '../AuthModal/AuthModal';
import { useStore } from '../../store';
import db, { auth } from '../../firebase';

export default function Sidebar() {
  const [open, setOpen] = useState(false);
  const { state, dispatch } = useStore();
  const { user } = state;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <AuthModal open={open} onClose={handleClose} />

      <nav className="fixed top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
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
      </nav>

      <aside
        id="logo-sidebar"
        className="fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full bg-white border-r border-gray-200 sm:translate-x-0 dark:bg-gray-800 dark:border-gray-700 justify-center items-center flex flex-col justify-between"
        aria-label="Sidebar"
      >
        <div className="flex flex-col mt-12 justify-center items-center">
          <div className="px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800">
            <img src={aclLogo} className="h-[150px]" />
          </div>
          <p className="text-white text-center">
            A simple tool to parse your paper, help fill the ACL responsible checklist, and avoid a desk rejection
          </p>
          <div className="flex flex-row mt-4">
            <button className="text-white m-1 w-full border-2 px-2 rounded-lg">Upload paper</button>
            <button className="text-black bg-white rounded-lg m-1 w-full">Export Response</button>
          </div>
        </div>
        <div className="flex flex-col w-full justify-center items-center">
          <h1 className="text-white text-xl">Issue Inspector</h1>
          <hr className="text-white m-5 w-1/3" />
          <div className="h-[12pc] bg-black w-full cursor-pointer overflow-scroll py-2">
            <h1 className="text-white">Upload paper to view results...</h1>
          </div>
        </div>
      </aside>
    </>
  );
}
