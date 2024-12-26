import streamlit as st
import os, json
from dotenv import load_dotenv
from mistralai import Mistral
from neo4j import GraphDatabase

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("MISTRAL_API_KEY")
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')
# Initialize Mistral client
mistral_client = Mistral(api_key=api_key)
# Initialize Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def process_prompt(text):
    """
    Process a prompt using the Mistral agent and return the response.

    Args:
    text (str): The input prompt from the user.

    Returns:
    str: The response from the Mistral agent.
    """
    chat_response = mistral_client.agents.complete(
        agent_id=os.getenv('AGENT_KEY'),
        messages=[
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return chat_response.choices[0].message.content

# Streamlit app configuration
st.set_page_config(layout="wide")
st.title("📄 Q&A Chatbot for Contract Review")

# Chat Section
st.subheader("Chat with Your Agent")
chat_placeholder = st.container()

# Placeholder for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
def display_chat():
    with chat_placeholder:
        for chat in st.session_state.chat_history:
            if chat['role'] == 'user':
                st.markdown(f"**User:** {chat['content']}") 
            else:
                st.markdown(f"**Agent:** {chat['content']}")

# Input form for chat
with st.form(key="chat_form"):
    user_input = st.text_input("Enter your question:", "")
    send_button = st.form_submit_button("Send")

# Handle chat submission
if send_button and user_input.strip():
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Get agent response from Mistral Agent
    agent_response = process_prompt(user_input)
    st.session_state.chat_history.append({"role": "agent", "content": agent_response})

    # Update chat display
    display_chat()

# Footer
st.markdown("---")
st.write("© 2024 Your Company Name. All rights reserved.")