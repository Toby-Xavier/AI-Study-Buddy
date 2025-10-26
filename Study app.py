# Import necessary libraries for the application
import streamlit as st  # Main library for creating web apps
import openai  # Library for interacting with OpenAI/Azure OpenAI API
import os  # Library for accessing environment variables
from datetime import datetime  # For getting current timestamp

# Remember to set these environment variables in the terminal before running:
# export AZURE_OPENAI_KEY="your-key-here"
# export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
# export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"

# Configure Azure OpenAI API settings
openai.api_type = "azure"  # Specify we're using Azure OpenAI (not standard OpenAI)
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # Get API endpoint from environment variable
openai.api_key = os.getenv("AZURE_OPENAI_KEY")  # Get API key from environment variable
openai.api_version = "2024-02-01-preview"  # Specify which API version to use

# Get the deployment name from environment variables
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

# Configure Streamlit page settings
st.set_page_config(
    page_title="Your Study Buddy",  # Text shown in browser tab
    page_icon="🎓",  # Emoji icon shown in browser tab
    layout="centered"  # Layout style for the page
)

# Add custom CSS styles to make the chat interface look nice
st.markdown("""
    <style>
    body {
        background-color: #f9fafb;  /* Light gray background for the whole page */
    }
    .chat-message {
        border-radius: 12px;  /* Rounded corners for message bubbles */
        padding: 12px;  /* Space inside message bubbles */
        margin-bottom: 8px;  /* Space between messages */
        max-width: 85%;  /* Messages don't take full width */
    }
    .user-message {
        background-color: #DCF8C6;  /* Light green background for user messages */
        text-align: right;  /* Align user text to the right */
        margin-left: auto;  /* Push user messages to the right side */
    }
    .assistant-message {
        background-color: #FFFFFF;  /* White background for assistant messages */
        text-align: left;  /* Align assistant text to the left */
        margin-right: auto;  /* Keep assistant messages on the left side */
        border: 1px solid #ddd;  /* Light gray border around assistant messages */
    }
    .timestamp {
        font-size: 0.75rem;  /* Small text size for timestamps */
        color: #888;  /* Gray color for timestamps */
    }
    </style>
""", unsafe_allow_html=True)  # Allow HTML rendering for custom styles

# Create the main title and description for the app
st.title("🎓 Your Study Buddy")  # Main heading with graduation cap emoji
st.write("Ask me any question let's prepare for your certification or university exams together!")  # Subtitle text

# Initialize session state to store chat messages
# Session state preserves data across user interactions
if "messages" not in st.session_state:  # Check if messages list doesn't exist yet
    st.session_state["messages"] = []  # Create empty list to store chat messages

# Display all previous chat messages from session state
for msg in st.session_state["messages"]:  # Loop through each message in history
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"  # Choose CSS class based on who sent message
    with st.container():  # Create a container for each message
        st.markdown(  # Render the message with HTML styling
            f'<div class="chat-message {role_class}">{msg["content"]}</div>'  # Message bubble with content
            f'<div class="timestamp">{msg["time"]}</div>',  # Timestamp below message
            unsafe_allow_html=True  # Allow HTML tags in the message
        )

# Create chat input widget at the bottom of the screen
user_input = st.chat_input("Type your question or exam...")  # Input field with placeholder text

# Check if user has entered a new message
if user_input:  # This block runs only when user sends a message
    
    # Save user message to session state
    user_msg = {
        "role": "user",  # Identify this as a user message
        "content": user_input,  # The actual text user typed
        "time": datetime.now().strftime("%H:%M")  # Current time in HH:MM format
    }
    st.session_state["messages"].append(user_msg)  # Add message to chat history

    # Show user message immediately in the chat interface
    with st.container():  # Create container for the new message
        st.markdown(f'<div class="chat-message user-message">{user_input}</div>', unsafe_allow_html=True)  # Display user message

    # Prepare message history for sending to Azure OpenAI
    chat_history = [{"role": "system", "content": "You are a helpful study assistant for exam preparation."}]  # System prompt that guides AI behavior
    for m in st.session_state["messages"]:  # Add all previous messages to context
        chat_history.append({"role": m["role"], "content": m["content"]})  # Copy each message to API format

    # Get AI response from Azure OpenAI
    with st.spinner("Thinking..."):  # Show loading spinner while waiting for AI
        try:  # Try to get response from AI service
            response = openai.ChatCompletion.create(  # Send request to Azure OpenAI
                engine=DEPLOYMENT_NAME,  # Which AI model to use
                messages=chat_history,  # The conversation history
                temperature=0.7,  # Controls randomness: 0 = predictable, 1 = creative
                max_tokens=800  # Maximum length of AI response
            )
            ai_reply = response["choices"][0]["message"]["content"]  # Extract AI's text response

            # Save AI's reply to session state
            st.session_state["messages"].append({
                "role": "assistant",  # Identify this as an AI message
                "content": ai_reply,  # The AI's response text
                "time": datetime.now().strftime("%H:%M")  # Current timestamp
            })

            # Display AI's reply in the chat interface
            with st.container():  # Create container for AI message
                st.markdown(
                    f'<div class="chat-message assistant-message">{ai_reply}</div>'  # AI message bubble
                    f'<div class="timestamp">{datetime.now().strftime("%H:%M")}</div>',  # Timestamp
                    unsafe_allow_html=True  # Allow HTML in AI response
                )

        except Exception as e:  # Handle errors if AI service fails
            st.error(f"Error connecting to Azure OpenAI: {e}")  # Show error message to user