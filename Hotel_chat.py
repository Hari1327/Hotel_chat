import streamlit as st
import pandas as pd
import chromadb
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory

# Load CSV Data
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df[['utterance', 'intent', 'category', 'tags']]

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="customer_support")

# Load data into ChromaDB
def populate_chroma(df):
    for idx, row in df.iterrows():
        collection.add(ids=[str(idx)], documents=[row['utterance']], metadatas=[{"intent": row['intent'], "category": row['category'], "tags": row['tags']}])

data = load_data("/content/drive/MyDrive/Guvi_final_Project/CS Data/Bitext_Sample_Customer_Service_Training_Dataset.csv")
populate_chroma(data)

# Setup LLM (Groq API via OpenAI wrapper)
llm = ChatOpenAI(model_name="gpt-4", openai_api_key="GROQ_API_KEY")
retriever = Chroma(persist_directory="chroma_db", embedding_function=OpenAIEmbeddings()).as_retriever()

# LangChain Chatbot Chain
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

# Streamlit UI
st.title("Customer Support Chatbot")
st.write("Ask me anything about our services!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")
if user_input:
    response = qa_chain.run(user_input)
    st.session_state.chat_history.append((user_input, response))

    # Display chat history
    for user, bot in st.session_state.chat_history:
        st.write(f"**You:** {user}")
        st.write(f"**Bot:** {bot}")
