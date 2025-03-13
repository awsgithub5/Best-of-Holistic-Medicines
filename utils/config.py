#config.py
"""
Configuration and environment setup for the holistic medicine chatbot.
"""
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")

# App configuration
APP_TITLE = "Holistic Medicine Chatbot"
APP_ICON = "🌿"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Configure page settings
def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=SIDEBAR_STATE
    )
    
    # Apply custom CSS
    st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .treatment-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .treatment-header {
            color: #2c3e50;
            font-size: 1.4rem;
            margin-bottom: 10px;
        }
        .disease-card {
            background-color: #e6f3ff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .ayurvedic {
            background-color: #e8f5e9;
        }
        .homeopathic {
            background-color: #e3f2fd;
        }
        .allopathic {
            background-color: #fff3e0;
        }
        .symptom-tag {
            display: inline-block;
            background-color: #f1f1f1;
            padding: 5px 12px;
            margin: 5px;
            border-radius: 20px;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)