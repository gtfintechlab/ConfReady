import concurrent.futures
from langchain_community.document_loaders import DirectoryLoader
#from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_together.embeddings import TogetherEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate

PDF_DIRECTORY_PATH = 'assets/docs'
VECTOR_DB_PATH = 'assets/database'
TOGETHER_API_KEY = '7fccdc0356437b145d9b3b3583bd963d1230b0c3987fdb0f7e7ec6c9dc84c564'
EMBEDDING_MODEL_NAME = 'togethercomputer/m2-bert-80M-8k-retrieval'

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def load_documents() -> list[Document]:
    """
    Load documents from the specified directory.
    
    Returns:
        list[Document]: List of loaded documents.
    """

    document_loader = DirectoryLoader(PDF_DIRECTORY_PATH)
    return document_loader.load()

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into smaller chunks for better processing.
    
    Args:
        documents (list[Document]): List of documents to split.
    
    Returns:
        list[Document]: List of split document chunks.
    """

    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True
        )
    
    return text_splitter.split_documents(documents)

def embeddings_function() -> TogetherEmbeddings:
    """
    Initialize the embeddings function with the specified API key and model.
    
    Returns:
        TogetherEmbeddings: Configured embeddings function.
    """
    embeddings = TogetherEmbeddings(api_key= TOGETHER_API_KEY)
    return embeddings

def create_vector_database(documents: list[Document]):
    """
    Create a vector database from the provided documents.
    
    Args:
        documents (list[Document]): List of documents to add to the vector database.
    """
    db = Chroma(
        persist_directory= VECTOR_DB_PATH,
        embedding_function= embeddings_function()
    )

    db.add_documents(documents)
    db.persist()

def query_rag(query: str) -> str:
    """
    Query the vector database using Retrieval-Augmented Generation (RAG).
    
    Args:
        query (str): Query string to search for in the vector database.
    
    Returns:
        str: The response from the RAG model.
    """
    embedding_function = embeddings_function()
    db = Chroma(persist_directory=VECTOR_DB_PATH, embedding_function=embedding_function)

    vector_response = db.similarity_search_with_score(query, k = 20)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in vector_response])

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    client = Together(api_key=TOGETHER_API_KEY)

    response = client.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    messages=[{"role": "user", "content": prompt}],
                )
    
    return response.choices[0].message.content

def direct_load(query: str) -> str:

    documents = load_documents()

    client = Together(api_key=TOGETHER_API_KEY)

    response = client.chat.completions.create(
                    model="meta-llama/Llama-3-70b-chat-hf",
                    messages=[{"role": "user", "content": prompt}],
                )
    
    return response.choices[0].message.content
    
def main():
    print('PDF Found')
    print(len(load_documents()))
    documents = split_documents(load_documents())
    print(f'PDF -> {len(documents)} Chunks')

    # create_vector_database(documents)
    print('Vector DB Created')

    # query = '''
    #     Given the PDF file, 
    #     extract the names of the authors of the paper. The authors' names are 
    #     typically found on the first page of the document, near the title or abstract. 
    #     Please provide the list of authors in the order they appear in the document. 
    # '''

    query = 'Do the abstract and introduction summarize the paper’s main claims?'
    
    print(query_rag(query))

main()