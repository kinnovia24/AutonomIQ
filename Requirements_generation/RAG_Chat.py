# ## RAG Q&A Conversation With PDF Including Chat History
# import streamlit as st
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_chroma import Chroma
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_openai import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# import os

# from dotenv import load_dotenv
# load_dotenv()

# # os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
# # embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")
# embeddings = OpenAIEmbeddings(model="text-embedding-3-large")



# ## set up Streamlit 

# st.set_page_config(page_title="Automotive RAG", layout="wide")
# st.title("🚗 Automotive RAG")
# st.write("Upload Pdf's and chat with their content")


# st.sidebar.page_link("pages/contentpage.py", label="PDF Data Extractor 📄")


# ## Input the Groq API Key
# api_key="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"

# ## Check if groq api key is provided
# if api_key:
#     llm=ChatGroq(groq_api_key=api_key,model_name="deepseek-r1-distill-llama-70b")
#     # llm=ChatOpenAI(api_key=api_key, model='gpt-4o')

#     ## chat interface
#     session_id = "default_session"
#     # session_id=st.text_input("Session ID",value="default_session")
#     ## statefully manage chat history

#     if 'store' not in st.session_state:
#         st.session_state.store={}

#     uploaded_files=st.file_uploader("Choose A PDf file",type="pdf",accept_multiple_files=True)
#     ## Process uploaded  PDF's
#     if uploaded_files:
#         documents=[]
#         for uploaded_file in uploaded_files:
#             temppdf=f"./temp.pdf"
#             with open(temppdf,"wb") as file:
#                 file.write(uploaded_file.getvalue())
#                 file_name=uploaded_file.name

#             loader=PyPDFLoader(temppdf)
#             docs=loader.load()
#             documents.extend(docs)

#     # Split and create embeddings for the documents
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
#         splits = text_splitter.split_documents(documents)
#         vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")
#         retriever = vectorstore.as_retriever()    

#         contextualize_q_system_prompt=(
#             "Given a chat history and the latest user question"
#             "which might reference context in the chat history, "
#             "formulate a standalone question which can be understood "
#             "without the chat history. Do NOT answer the question, "
#             "just reformulate it if needed and otherwise return it as is."
#         )
#         contextualize_q_prompt = ChatPromptTemplate.from_messages(
#                 [
#                     ("system", contextualize_q_system_prompt),
#                     MessagesPlaceholder("chat_history"),
#                     ("human", "{input}"),
#                 ]
#             )
        
#         history_aware_retriever=create_history_aware_retriever(llm,retriever,contextualize_q_prompt)

#         ## Answer question

#         # Answer question
#         system_prompt = (
#                 "You are an assistant for Automotive embedded software developer for question-answering tasks. "
#                 "Use the following pieces of retrieved context to answer "
#                 "the question. If you don't know the answer, say that you "
#                 "don't know. Use three sentences maximum and keep the "
#                 "answer concise. And dont repeat the same points and keep it unique and precise."
#                 "\n\n"
#                 "{context}"
#             )
#         qa_prompt = ChatPromptTemplate.from_messages(
#                 [
#                     ("system", system_prompt),
#                     MessagesPlaceholder("chat_history"),
#                     ("human", "{input}"),
#                 ]
#             )
        
#         question_answer_chain=create_stuff_documents_chain(llm,qa_prompt)
#         rag_chain=create_retrieval_chain(history_aware_retriever,question_answer_chain)

#         def get_session_history(session:str)->BaseChatMessageHistory:
#             if session_id not in st.session_state.store:
#                 st.session_state.store[session_id]=ChatMessageHistory()
#             return st.session_state.store[session_id]
        
#         conversational_rag_chain=RunnableWithMessageHistory(
#             rag_chain,get_session_history,
#             input_messages_key="input",
#             history_messages_key="chat_history",
#             output_messages_key="answer"
#         )

#         user_input = st.text_input("Your question:")
#         if user_input:
#             session_history=get_session_history(session_id)
#             response = conversational_rag_chain.invoke(
#                 {"input": user_input},
#                 config={
#                     "configurable": {"session_id":session_id}
#                 },  # constructs a key "abc123" in `store`.
#             )
#             # st.write(st.session_state.store)
#             st.write("Assistant:", response['answer'])
#             # st.write("Chat History:", session_history.messages)
# else:
#     st.warning("Press Enter")




import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import create_history_aware_retriever
from langchain import hub
import os
import uuid

from dotenv import load_dotenv
load_dotenv()

def show_rag_chat():
    """Displays the RAG Chat UI in Streamlit"""
    
    # Load API Keys
    # os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
    # embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Streamlit UI
    # st.set_page_config(page_title="Automotive RAG", layout="wide")
    st.title("Specifications Intelligence")
    st.write("Upload specification document ask AI about content")

    # Retrieve API Key Securely
    api_key = "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"
    # api_key = "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"
    if not api_key:
        st.error("Missing API Key. Please set GROQ_API_KEY in your .env file.")
        return
    
    # Initialize LLM
    llm = ChatGroq(groq_api_key=api_key, model_name="deepseek-r1-distill-llama-70b")

    # Session Handling
    session_id = "default_session"
    if 'store' not in st.session_state:
        st.session_state.store = {}

    # File Upload
    uploaded_files = st.file_uploader("Choose a PDF file", type=["pdf"], accept_multiple_files=True)

    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            temp_pdf_path = f"./temp_{uuid.uuid4()}.pdf"  # Unique filename to prevent overwriting
            with open(temp_pdf_path, "wb") as file:
                file.write(uploaded_file.getvalue())

            loader = PyPDFLoader(temp_pdf_path)
            docs = loader.load()
            documents.extend(docs)

        # Text Splitting & Vector Storage
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=500)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory="./chroma_db")
        retriever = vectorstore.as_retriever()

        # Contextualizing User Queries
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Reformulate a standalone question from the chat history."),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

        # Question Answering Prompt
        system_prompt = (
            "You are an assistant for Automotive embedded software developers who is good at generating the AUTOSAR and ASPICE standard test cases and code which is compliant. "
            "Use the retrieved context to answer the question concisely."
            "\n\n"
            "{context}"
        )
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        
        # Build RAG Chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # Session History Function
        def get_session_history(session: str) -> BaseChatMessageHistory:
            if session not in st.session_state.store:
                st.session_state.store[session] = ChatMessageHistory()
            return st.session_state.store[session]

        # Attach History to RAG
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain, get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        # User Input & Response Handling
        user_input = st.text_input("Your question:")
        if user_input:
            session_history = get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )
            st.write("Assistant:", response['answer'])

if __name__ == "__main__":
    show_rag_chat()
