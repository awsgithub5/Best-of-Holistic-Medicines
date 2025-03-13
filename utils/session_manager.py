#session_manager.py
"""
Streamlit session state management for the holistic medicine chatbot.
"""
import streamlit as st
import re
from utils.symptom_analyzer import symptom_preprocess

def initialize_session_state():
    """
    Initialize all required session state variables.
    """
    if 'selected_symptoms' not in st.session_state:
        st.session_state.selected_symptoms = []
    if 'detected_diseases' not in st.session_state:
        st.session_state.detected_diseases = {}
    if 'selected_disease' not in st.session_state:
        st.session_state.selected_disease = None
    if 'treatment_view' not in st.session_state:
        st.session_state.treatment_view = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'llm_mode' not in st.session_state:
        st.session_state.llm_mode = False
    if 'symptom_input' not in st.session_state:
        st.session_state.symptom_input = ""
    if 'selected_suggestion' not in st.session_state:
        st.session_state.selected_suggestion = ""

# Callback functions for handling input changes
def set_symptom_input(value):
    """Update symptom input value in session state."""
    st.session_state.symptom_input = value

def add_symptom():
    """Add current symptom input to selected symptoms list."""
    if st.session_state.symptom_input:
        # Process potential compound symptoms
        new_symptoms = symptom_preprocess(st.session_state.symptom_input)
        
        for symptom in new_symptoms:
            if symptom and symptom not in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.append(symptom)
        
        st.session_state.symptom_input = ""

def add_suggested_symptom():
    """Add the selected suggestion to symptoms list."""
    if st.session_state.selected_suggestion and st.session_state.selected_suggestion not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(st.session_state.selected_suggestion)
        st.session_state.symptom_input = ""
        st.session_state.selected_suggestion = ""

def add_common_symptom(symptom):
    """Add a common predefined symptom to the list."""
    if symptom not in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.append(symptom)

def remove_symptom(symptom):
    """Remove a symptom from the selected list."""
    if symptom in st.session_state.selected_symptoms:
        st.session_state.selected_symptoms.remove(symptom)

def clear_symptoms():
    """Clear all selected symptoms and related state."""
    st.session_state.selected_symptoms = []
    st.session_state.detected_diseases = {}
    st.session_state.selected_disease = None

def set_selected_disease(disease):
    """Set the currently selected disease."""
    st.session_state.selected_disease = disease

def set_treatment_view(view):
    """Set the treatment view type."""
    st.session_state.treatment_view = view

def add_to_chat_history(role, content):
    """Add a message to the chat history."""
    st.session_state.chat_history.append({"role": role, "content": content})

def toggle_llm_mode(value):
    """Toggle the LLM enhanced mode."""
    st.session_state.llm_mode = value