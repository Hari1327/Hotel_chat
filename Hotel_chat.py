# app.py
import os
import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize components
def initialize_components():
    # Load CSV data
    df = pd.read_csv('Bitext_Sample_Customer_Service_Training_Dataset.csv')  # Update with your CSV path
    
    # Initialize embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create ChromaDB vector store
    vector_store = Chroma.from_texts(
        texts=df['utterance'].tolist(),
        embedding=embeddings,
        metadatas=df[['intent', 'category', 'tags']].to_dict('records')
    )
    
    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="mixtral-8x7b-32768"
    )
    
    return vector_store, llm

# Create prompt template
def create_prompt_template():
    template = """
    You're a customer support assistant. Use the following context to help the user:
    
    Context:
    {context}
    
    User Question: {question}
    
    Provide a helpful and professional response:
    """
    return PromptTemplate(template=template, input_variables=["context", "question"])

# Main app
def main():
    st.title("Customer Support Chatbot")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Initialize components
    vector_store, llm = initialize_components()
    prompt_template = create_prompt_template()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if user_input := st.chat_input("How can I help you today?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Retrieve relevant context
        results = vector_store.similarity_search(user_input, k=3)
        context = "\n".join([
            f"Utterance: {doc.page_content}\nIntent: {doc.metadata['intent']}\nCategory: {doc.metadata['category']}"
            for doc in results
        ])
        
        # Generate response
        chain = prompt_template | llm
        response = chain.invoke({"context": context, "question": user_input})
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.content})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.content)

if __name__ == "__main__":
    main()
