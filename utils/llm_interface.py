#llm_interface.py
"""
Azure OpenAI integration for the holistic medicine chatbot.
"""
import streamlit as st
from openai import AzureOpenAI

def initialize_azure_client(api_key, endpoint, api_version):
    """
    Initialize the Azure OpenAI client.
    
    Args:
        api_key (str): Azure OpenAI API key
        endpoint (str): Azure OpenAI endpoint
        api_version (str): Azure OpenAI API version
        
    Returns:
        AzureOpenAI: Initialized client or None if unsuccessful
    """
    try:
        if api_key and endpoint:
            client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            return client
        else:
            return None
    except Exception as e:
        st.error(f"Error initializing Azure OpenAI client: {str(e)}")
        return None

def get_llm_response(client, deployment, prompt, max_tokens=1000):
    """
    Get a response from the Azure OpenAI model.
    
    Args:
        client (AzureOpenAI): Azure OpenAI client
        deployment (str): Azure deployment name
        prompt (str): Prompt to send to the model
        max_tokens (int): Maximum tokens in the response
        
    Returns:
        str: Model response
    """
    try:
        if not client:
            return "Azure OpenAI not configured. Please set the required environment variables."
        
        # Using chat completions with proper format (messages array)
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error getting LLM response: {str(e)}"

def process_natural_language_symptoms(client, deployment, user_input):
    """
    Extract symptoms from natural language description.
    
    Args:
        client (AzureOpenAI): Azure OpenAI client
        deployment (str): Azure deployment name
        user_input (str): User's natural language description
        
    Returns:
        tuple: (extracted_symptoms, error)
    """
    if not client:
        return [], "Azure OpenAI not configured. Please set the required environment variables."
    
    try:
        prompt = f"""
        Extract specific medical symptoms from the following text. Return ONLY a comma-separated list of symptoms, without any additional text.
        For example, if the input is "I've been feeling dizzy and nauseous since yesterday", return "dizziness, nausea".
        
        User text: {user_input}
        
        Symptoms:
        """
        
        response = get_llm_response(client, deployment, prompt)
        extracted_symptoms = [s.strip() for s in response.split(',')]
        return extracted_symptoms, None
    except Exception as e:
        return [], f"Error processing symptoms: {str(e)}"

def enhance_treatment_description(client, deployment, treatment_type, base_treatment, disease, symptoms):
    """
    Enhance treatment description with more details.
    
    Args:
        client (AzureOpenAI): Azure OpenAI client
        deployment (str): Azure deployment name
        treatment_type (str): Type of treatment (Ayurvedic, Homeopathic, Allopathic)
        base_treatment (str): Original treatment description
        disease (str): Disease name
        symptoms (str): Disease symptoms
        
    Returns:
        str: Enhanced treatment description
    """
    if not client:
        return base_treatment
    
    try:
        prompt = f"""
        Enhance this {treatment_type} treatment description for {disease} with more detailed explanations, 
        including potential benefits and considerations. Keep the response under 250 words, be factual, 
        and maintain a professional tone.
        
        Disease: {disease}
        Symptoms: {symptoms}
        Base treatment: {base_treatment}
        
        Enhanced treatment explanation:
        """
        
        enhanced_description = get_llm_response(client, deployment, prompt)
        return enhanced_description or base_treatment
    except Exception:
        return base_treatment