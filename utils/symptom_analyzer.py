#symptom_analyzer.py
"""
Disease prediction and symptom analysis for the holistic medicine chatbot.
"""
import re

def find_diseases(kb_data, input_symptoms):
    """
    Find diseases based on input symptoms.
    
    Args:
        kb_data (list): List of disease entries
        input_symptoms (list): List of symptoms
        
    Returns:
        dict: Dictionary of potential diseases with match scores
    """
    input_symptoms = [s.lower().strip() for s in input_symptoms]
    potential_diseases = {}
    
    for disease in kb_data:
        disease_name = disease['Disease']
        disease_symptoms = disease['Symptoms'].lower()
        
        # Process disease symptoms to individual terms for better matching
        disease_symptom_list = []
        for symptom in re.split(r'[,;]', disease_symptoms):
            disease_symptom_list.append(symptom.strip())
        
        # Count how many of the input symptoms match with this disease
        match_count = 0
        for user_symptom in input_symptoms:
            # Check for exact matches first
            if user_symptom in disease_symptoms:
                match_count += 1
                continue
                
            # Check for partial matches within disease symptoms
            for disease_symptom in disease_symptom_list:
                if user_symptom in disease_symptom or disease_symptom in user_symptom:
                    match_count += 1
                    break
                    
        # Calculate match score (percentage of input symptoms matched)
        if input_symptoms:  # Avoid division by zero
            match_percentage = (match_count / len(input_symptoms)) * 100
            if match_percentage > 0:
                potential_diseases[disease_name] = {
                    'score': match_percentage,
                    'category': disease['Category'],
                    'full_symptoms': disease['Symptoms']
                }
    
    # Sort by match score (highest first)
    return dict(sorted(potential_diseases.items(), key=lambda item: item[1]['score'], reverse=True))


def symptom_preprocess(symptom_text):
    """
    Preprocess symptom text to handle compound symptom entries.
    
    Args:
        symptom_text (str): Raw symptom text from user
        
    Returns:
        list: List of individual symptoms
    """
    # Handle common separators
    if ',' in symptom_text:
        return [s.strip() for s in symptom_text.split(',')]
    elif ';' in symptom_text:
        return [s.strip() for s in symptom_text.split(';')]
    elif '/' in symptom_text:
        return [s.strip() for s in symptom_text.split('/')]
    
    # Check for capitalization patterns that might indicate separate symptoms
    # e.g. "CoughFeverSore throat" -> ["Cough", "Fever", "Sore throat"]
    patterns = re.findall(r'[A-Z][a-z]+', symptom_text)
    if len(patterns) > 1:
        # Extract capitalized words as separate symptoms
        symptoms = []
        current_pos = 0
        for pattern in patterns:
            pattern_pos = symptom_text.find(pattern, current_pos)
            if pattern_pos > current_pos and current_pos > 0:
                # There's text between the last pattern and this one
                symptoms.append(symptom_text[current_pos:pattern_pos].strip())
            symptoms.append(pattern)
            current_pos = pattern_pos + len(pattern)
        
        # Add any remaining text
        if current_pos < len(symptom_text):
            symptoms.append(symptom_text[current_pos:].strip())
        
        return [s for s in symptoms if s]
    
    # If no clear separation, return as single symptom
    return [symptom_text]