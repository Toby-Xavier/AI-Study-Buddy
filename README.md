# AI Study Buddy Chatapp 

## Overview
A Streamlit web application that creates an AI-powered study assistant using Azure OpenAI. The app has a clean chat interface where users can ask questions and get help with exam preparation.

## Features
- AI-powered study assistant using Azure OpenAI
- Clean chat interface with message bubbles
- Timestamps for all messages
- Custom CSS styling for WhatsApp-like appearance
- Persistent chat history during session
- Real-time message display

## Prerequisites
- Python 3.7+
- Azure OpenAI account and deployment
- Required environment variables set

## Installation

1. Install required packages:
pip install streamlit openai

2. Set up environment variables:
export AZURE_OPENAI_KEY="your-azure-openai-key"
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"

## Running the Application

1. Save the code as study_buddy.py
2. Run the application:
streamlit run study_buddy.py
3. Open your browser to the displayed URL (typically http://localhost:8501)

## How It Works

### Core Components:
1. User Interface: Streamlit creates the web interface with custom CSS styling
2. Chat History: Session state preserves conversation across interactions
3. AI Integration: A trained Azure OpenAI GPT model generates responses
4. Message Display: Custom HTML/CSS creates chat bubble appearance

### Message Flow:
1. User types a question in the chat input
2. Message is saved to session state and displayed immediately
3. Full conversation history is sent to Azure OpenAI
4. Trained AI model generates a response based on the context
5. AI response is displayed and saved to chat history

## Configuration Options

### Azure OpenAI Settings:
- temperature=0.7: Controls response creativity (0-1)
- max_tokens=800: Limits response length
- API version: 2024-02-01-preview

### Customization:
- Modify system prompt to change AI behavior
- Adjust CSS styles for different appearance
- Change page title and icon in set_page_config

## Troubleshooting

### Common Issues:
1. Environment variables not set: Ensure all three required variables are exported
2. Azure deployment issues: Verify deployment name and endpoint URL
3. API errors: Check Azure OpenAI quota and deployment status

### Error Handling:
- Connection errors display user-friendly messages
- Invalid API keys show clear error information
- Network issues trigger retry mechanisms

## Security Notes
- API keys are stored in environment variables (not in code)
- No data persistence beyond current session
- Azure OpenAI provides enterprise-grade security

## Support
For issues with:
- Azure OpenAI: Check Azure portal and documentation
- Streamlit: Visit https://docs.streamlit.io
- Application code: Review environment variables and deployment settings
