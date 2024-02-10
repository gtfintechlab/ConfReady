import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface ModelState {
  name: string;
  authors: string;
  tempMarkdown: string;
  provideCode: boolean;
  provideData: boolean;
}

// Create the Zustand store with middleware
export const useModelStore = create<ModelState>(
  persist(
    devtools((set, get) => ({
      // Initial state values
      name: '',
      authors: '',
      tempMarkdown: '',
      provideCode: '',
      provideData: '',
      datasetSummary: '',

      // Concise state update functions using arrow functions
      setName: (nameItem: string) => set((state) => ({ ...state, name: nameItem })),
      setAuthors: (authorsItem: string) => set((state) => ({ ...state, authors: authorsItem })),
      setTempMarkdown: (tempMarkdownItem: string) =>
        set((state) => ({ ...state, tempMarkdown: tempMarkdownItem })),
      setProvideCode: (provideCodeItem: string) =>
        set((state) => ({ ...state, provideCode: provideCodeItem })),
      setProvideData: (provideDataItem: string) =>
        set((state) => ({ ...state, provideData: provideDataItem })),
        setDatasetSummary: (datasetSummaryItem: string) =>
        set((state) => ({ ...state, datasetSummary: datasetSummaryItem })),
    })),
    {
      name: 'modelCard-storage',
    }
  )
);
