#ui_components.py
"""
UI components and layout helpers for the holistic medicine chatbot.
"""
import streamlit as st
import re
from utils.session_manager import (
    set_symptom_input, add_symptom, add_suggested_symptom, 
    add_common_symptom, remove_symptom, clear_symptoms,
    set_selected_disease, set_treatment_view, add_to_chat_history
)
from utils.symptom_analyzer import symptom_preprocess

def render_header():
    """Render application header and introduction."""
    st.title("🌿 Holistic Medicine Chatbot")
    st.markdown("""
    This chatbot provides treatment suggestions from Ayurvedic, Homeopathic, and Allopathic medicine systems.
    Enter your symptoms below to get started.
    """)

def render_sidebar(
    llm_mode, 
    client, 
    deployment, 
    all_symptoms, 
    process_nl_symptoms_fn
):
    """
    Render sidebar with symptom input options.
    
    Args:
        llm_mode (bool): Whether LLM mode is enabled
        client: Azure OpenAI client
        deployment (str): Azure deployment name
        all_symptoms (list): List of all symptoms
        process_nl_symptoms_fn: Function to process natural language symptoms
    """
    with st.sidebar:
        st.header("Symptom Selection")
        
        # Toggle for LLM enhanced mode
        llm_mode_toggle = st.toggle("Enable AI-Enhanced Mode", llm_mode)
        if llm_mode_toggle != llm_mode:
            st.session_state.llm_mode = llm_mode_toggle
        
        if st.session_state.llm_mode and not client:
            st.warning("⚠️ Azure OpenAI not configured. Please set the required Azure OpenAI environment variables.")
        
        # Natural language input section (when LLM mode is enabled)
        if st.session_state.llm_mode:
            render_nl_input(client, deployment, process_nl_symptoms_fn)
        
        render_manual_symptom_input(all_symptoms)
        render_common_symptoms()
        render_selected_symptoms()
        render_symptom_actions()

def render_nl_input(client, deployment, process_nl_symptoms_fn):
    """Render natural language symptom input section."""
    st.subheader("Describe Your Symptoms")
    nl_symptoms = st.text_area(
        "Describe how you feel in your own words:", 
        placeholder="Example: I've been having a headache and fever since yesterday, and my throat feels sore."
    )
    
    if nl_symptoms and st.button("Process Description"):
        with st.spinner("Analyzing your description..."):
            extracted_symptoms, error = process_nl_symptoms_fn(client, deployment, nl_symptoms)
            if error:
                st.error(error)
            elif extracted_symptoms:
                for symptom in extracted_symptoms:
                    if symptom and symptom not in st.session_state.selected_symptoms:
                        st.session_state.selected_symptoms.append(symptom)
                st.success(f"Extracted symptoms: {', '.join(extracted_symptoms)}")
                add_to_chat_history("user", nl_symptoms)
                add_to_chat_history("assistant", f"I've identified these symptoms: {', '.join(extracted_symptoms)}")
            else:
                st.warning("No clear symptoms detected. Please be more specific about your symptoms.")

def render_manual_symptom_input(all_symptoms):
    """Render manual symptom input section."""
    st.subheader("Add Individual Symptoms")
    
    # Help text for symptom input
    st.markdown("""
    <small>You can enter multiple symptoms at once using commas (e.g., "cough, fever, headache")</small>
    """, unsafe_allow_html=True)
    
    # Option to enter symptoms manually
    new_symptom = st.text_input(
        "Enter a symptom:", 
        value=st.session_state.symptom_input, 
        key="symptom_text_input",
        help="Type a symptom and press Enter to add it. You can enter multiple symptoms separated by commas.",
        on_change=set_symptom_input,
        args=(st.session_state.symptom_input,)
    )
    
    # Suggest symptoms as user types
    if new_symptom and len(new_symptom) > 2 and ',' not in new_symptom:
        from utils.kb_manager import suggest_symptoms
        suggestions = suggest_symptoms(all_symptoms, new_symptom)
        if suggestions:
            selected_suggestion = st.selectbox("Did you mean:", [""] + suggestions, key="suggestion_select")
            st.session_state.selected_suggestion = selected_suggestion
            if selected_suggestion and st.button("Add This Symptom", key="add_suggested"):
                add_suggested_symptom()
    
    # Add button for manual entry
    if new_symptom and st.button("Add Symptom", key="add_direct"):
        st.session_state.symptom_input = new_symptom  # Update session state
        add_symptom()

def render_common_symptoms():
    """Render common symptoms selection section."""
    st.subheader("Common Symptoms")
    common_symptoms = [
        "Fever", "Headache", "Cough", "Fatigue", "Sore throat", 
        "Runny nose", "Nausea", "Joint pain", "Abdominal pain",
        "Chest pain", "Shortness of breath", "Dizziness",
        "Rash", "Swelling", "Anxiety", "Depression", "Insomnia"
    ]
    
    # Display in a more compact way - 3 columns
    cols = st.columns(3)
    for i, symptom in enumerate(common_symptoms):
        col_idx = i % 3
        button_key = f"common_{i}"
        if cols[col_idx].button(symptom, key=button_key):
            add_common_symptom(symptom)

def render_selected_symptoms():
    """Render list of currently selected symptoms."""
    if st.session_state.selected_symptoms:
        st.subheader("Your Selected Symptoms")
        for i, symptom in enumerate(st.session_state.selected_symptoms):
            cols = st.columns([4, 1])
            cols[0].write(f"• {symptom}")
            remove_key = f"remove_{i}"
            if cols[1].button("✕", key=remove_key):
                remove_symptom(symptom)
                st.rerun()


def render_treatment_options(treatment_info, llm_mode, client, deployment):
    """
    Render treatment options for selected disease.
    
    Args:
        treatment_info (dict): Treatment information
        llm_mode (bool): Whether LLM mode is enabled
        client: Azure OpenAI client
        deployment (str): Azure deployment name
    """
    import streamlit as st
    from utils.session_manager import set_treatment_view
    
    st.header(f"Treatment Options for {st.session_state.selected_disease}")
    st.subheader(f"Category: {treatment_info['Category']}")
    st.write(f"**Common Symptoms:** {treatment_info['Symptoms']}")
    
    # Treatment view selection
    st.write("Choose a treatment approach:")
    
    # Set up the treatment view with buttons
    treatment_buttons = st.columns(4)
    
    if treatment_buttons[0].button("All Approaches", type="primary" if st.session_state.treatment_view == "all" else "secondary"):
        set_treatment_view("all")
        st.rerun()
        
    if treatment_buttons[1].button("Ayurvedic", type="primary" if st.session_state.treatment_view == "ayurvedic" else "secondary"):
        set_treatment_view("ayurvedic")
        st.rerun()
        
    if treatment_buttons[2].button("Homeopathic", type="primary" if st.session_state.treatment_view == "homeopathic" else "secondary"):
        set_treatment_view("homeopathic")
        st.rerun()
        
    if treatment_buttons[3].button("Allopathic", type="primary" if st.session_state.treatment_view == "allopathic" else "secondary"):
        set_treatment_view("allopathic")
        st.rerun()
    
    # Set default view if none selected
    if st.session_state.treatment_view is None:
        set_treatment_view("all")

def render_symptom_actions():
    """Render symptom action buttons (clear all, analyze)."""
    if st.session_state.selected_symptoms:
        # Clear all symptoms button
        if st.button("Clear All Symptoms"):
            clear_symptoms()
            st.rerun()
        
        # Analyze symptoms button
        if st.button("Analyze Symptoms", type="primary"):
            from utils.symptom_analyzer import find_diseases
            from utils.kb_manager import load_knowledge_base
            
            with st.spinner("Analyzing your symptoms..."):
                kb_data = load_knowledge_base()
                st.session_state.detected_diseases = find_diseases(kb_data, st.session_state.selected_symptoms)
                st.session_state.selected_disease = None
                st.session_state.treatment_view = None
                st.rerun()

def render_welcome_screen():
    """Render welcome screen with medicine system descriptions."""
    st.info("👈 Please select or enter your symptoms in the sidebar to get treatment recommendations.")
    
    # Display some information about the three medicine systems
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='treatment-card ayurvedic'>
            <h3 class='treatment-header'>🌿 Ayurvedic Medicine</h3>
            <p>Traditional Indian system of medicine dating back thousands of years. It focuses on holistic wellness through balance of doshas (vata, pitta, kapha) using herbs, diet, lifestyle, and cleansing practices.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class='treatment-card homeopathic'>
            <h3 class='treatment-header'>💧 Homeopathic Medicine</h3>
            <p>Alternative medicine system based on "like cures like" principle. It uses highly diluted substances to trigger the body's natural healing system, treating the whole person rather than isolated symptoms.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class='treatment-card allopathic'>
            <h3 class='treatment-header'>💊 Allopathic Medicine</h3>
            <p>Modern conventional medicine that uses pharmacologically active agents or physical interventions to treat or suppress symptoms or pathophysiologic processes of diseases or conditions.</p>
        </div>
        """, unsafe_allow_html=True)

def render_analysis_results():
    """Render symptom analysis results."""
    st.header("Analysis Results")
    
    # Display selected symptoms
    st.write("Based on your symptoms:")
    symptom_cols = st.columns(4)
    for i, symptom in enumerate(st.session_state.selected_symptoms):
        with symptom_cols[i % 4]:
            st.markdown(f"<div class='symptom-tag'>{symptom}</div>", unsafe_allow_html=True)
    
    # Display potential diseases if any were found
    if st.session_state.detected_diseases:
        st.subheader("Potential Conditions")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            for disease, details in list(st.session_state.detected_diseases.items())[:5]:  # Show top 5
                score = details['score']
                category = details['category']
                
                # Create an expander for each disease
                with st.expander(f"{disease} ({category}) - {score:.0f}% match"):
                    st.write(f"**Full Symptoms:** {details['full_symptoms']}")
                    
                    if st.button("View Treatment Options", key=f"select_{disease}"):
                        set_selected_disease(disease)
                        st.rerun()
        
        with col2:
            st.info("""
            **Note:** These potential conditions are based on symptom matching.
            
            The percentage shows how many of your symptoms match with the condition.
            
            This is not a medical diagnosis. Please consult a healthcare professional for proper diagnosis.
            """)
    
    elif st.session_state.detected_diseases == {}:
        st.warning("No matching conditions found in our database for your symptoms. Please try adding more specific symptoms or consult a healthcare professional.")