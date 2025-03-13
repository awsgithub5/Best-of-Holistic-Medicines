#kb_manager.py
"""
Knowledge base loading and processing for the holistic medicine chatbot.
"""
import json
import re
import streamlit as st

@st.cache_data
def load_knowledge_base(file_path='data/kb.json'):
    """
    Load the knowledge base from a JSON file.
    
    Args:
        file_path (str): Path to the knowledge base file
        
    Returns:
        list: List of disease entries
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        st.error(f"Knowledge base file not found. Please make sure {file_path} is in the same directory as the app.")
        return []

@st.cache_data
def create_symptom_mapping(kb_data):
    """
    Create mappings of symptoms to diseases and extract all symptoms.
    
    Args:
        kb_data (list): List of disease entries
        
    Returns:
        tuple: (symptom_map, all_symptoms, disease_symptoms)
            - symptom_map: Dictionary mapping symptoms to diseases
            - all_symptoms: List of all unique symptoms
            - disease_symptoms: Dictionary mapping diseases to their symptoms
    """
    symptom_map = {}
    disease_symptoms = {}
    all_symptoms = set()
    
    for entry in kb_data:
        disease = entry['Disease']
        symptoms = entry['Symptoms'].lower()
        disease_symptoms[disease] = symptoms
        
        # Extract individual symptoms
        symptom_list = [s.strip() for s in re.split(r'[,;]', symptoms)]
        for symptom in symptom_list:
            all_symptoms.add(symptom)
            if symptom in symptom_map:
                symptom_map[symptom].append(disease)
            else:
                symptom_map[symptom] = [disease]
    
    return symptom_map, list(all_symptoms), disease_symptoms

def get_treatment_info(kb_data, disease_name):
    """
    Get treatment information for a specific disease.
    
    Args:
        kb_data (list): List of disease entries
        disease_name (str): Name of the disease
        
    Returns:
        dict: Treatment information or None if disease not found
    """
    for entry in kb_data:
        if entry['Disease'] == disease_name:
            return {
                'Ayurvedic': entry['Ayurvedic_Treatment'],
                'Homeopathic': entry['Homeopathic_Treatment'],
                'Allopathic': entry['Allopathic_Treatment'],
                'Category': entry['Category'],
                'Symptoms': entry['Symptoms']
            }
    return None

def suggest_symptoms(all_symptoms, partial_input):
    """
    Suggest symptoms based on partial input.
    
    Args:
        all_symptoms (list): List of all symptoms
        partial_input (str): Partial symptom input
        
    Returns:
        list: List of matching symptoms
    """
    partial_input = partial_input.lower()
    matches = []
    
    for symptom in all_symptoms:
        if partial_input in symptom.lower():
            matches.append(symptom)
    
    return matches[:5]  # Return top 5 matches