from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_classic.chains import RetrievalQA

# --- UI Setup ---
st.set_page_config(page_title="Gita GPT", layout="wide")
st.title("Bhagavad Gita AI Assistant")
st.markdown("---")

# --- Initialize Session State ---
if "vector_db" not in st.session_state:
    st.session_state.vector_db = None


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_db_path = "holywalls/spirtual_hymns/bg_db"

# 1. Load the PDF
loader = PyPDFLoader("holywalls/lord-krishna/The_Bhagavad_Gita.pdf")
docs = loader.load()

# 2. Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=100
)
chunks = text_splitter.split_documents(docs)

# Load chunks into Chroma and save to a local 'db' folder
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=vector_db_path
)

print(f"Successfully loaded {len(chunks)} chunks into ChromaDB.")

# --- Main Chat Interface ---
st.header("Ask Krishna")
query = st.text_input("I'm your guide. Ask me anything about to seek spiritual wisdom.")

if query:
    # if st.session_state.vector_db is None:
    #     st.error("Please upload and process a PDF first!")
    if vector_db:
        # Initialize Local LLM via Ollama
        llm = Ollama(model="llama3")
        
        # Setup RAG Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=st.session_state.vector_db.as_retriever(),
            return_source_documents=True
        )
        
        # Execute Query
        with st.spinner("Seeking wisdom..."):
            response = qa_chain.invoke({"query": query})
            
            st.subheader("Answer:")
            st.write(response["result"])
            
            with st.expander("View Source Verses"):
                for doc in response["source_documents"]:
                    st.info(f"Page {doc.metadata['page']}: {doc.page_content[:300]}...")

