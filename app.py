# %%writefile app.py
import nest_asyncio
nest_asyncio.apply()  # Patch asyncio to allow nested event loops

import torch  # Pre-import torch to avoid file watcher issues with dynamic attributes

import streamlit as st
from datetime import datetime
from backend import get_chatbot_response 

try:
    import sqlite3
    from pysqlite3 import dbapi2 as sqlite3
except ImportError:
    pass

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())
# Inject custom CSS for a refined chatbot UI with royal colors
st.markdown(
    """
    <style>

    /* Container for the chat history */
    .chat-container {
        max-width: 800px;
        margin: auto;
        margin-top: 20px;
        padding: 10px;
        background-color: #F0F0F0;
        border-radius: 10px;
    }
    /* User message bubble - queries aligned left */
    .chat-message.user {
        background-color: #333333;  /* light lavender-blue */
        color: #ffffff;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: left;
        max-width: 70%;
        margin-right: auto;
    }
    /* Bot message bubble - answers aligned right */
    .chat-message.bot {
        background-color: #2A2F45;  /* royal blue */
        color: #fff;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: left;
        max-width: 70%;
        margin-left: auto;
    }
    /* Timestamp styling */
    .chat-time {
        font-size: 0.8rem;
        color: #ccc;
        margin-top: 5px;
    }
    /* Header styling with a royal tone */
    .header {
        text-align: center;
        padding: 15px;
        background-color: #2A2F45;  /* dark royal */
        color: #fff;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

def display_chat_message(speaker, message, timestamp):
    """
    Display a chat message with custom CSS.
    The user's query is aligned left, while the bot's answer is aligned right.
    """
    # Determine which CSS class to use based on the speaker
    bubble_class = "chat-message user" if speaker.lower() == "you" else "chat-message bot"
    html_content = f"""
    <div class="{bubble_class}">
        <p>{message}</p>
        <div class="chat-time">{timestamp}</div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def main():
    st.markdown('<div class="header"><h1>UTA Chatbot</h1><p>Your Personal Assistant for UTA Information</p></div>', unsafe_allow_html=True)
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Input for user's query
    user_query = st.text_input("Enter your question here:", key="user_input")
    
    if st.button("Submit") and user_query:
        with st.spinner("Processing your query..."):
            # Get the answer using the backend function
            response = get_chatbot_response(user_query)
            timestamp = datetime.now().strftime("%I:%M %p")
            st.session_state.chat_history.append(("You", user_query, timestamp))
            st.session_state.chat_history.append(("Bot", response, timestamp))
    
    # Display the conversation history within the chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for speaker, message, timestamp in st.session_state.chat_history:
        display_chat_message(speaker, message, timestamp)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

