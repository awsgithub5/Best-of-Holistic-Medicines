#app.py

#@shrina.neema
"""
Main file for the Holistic Medicine Chatbot application.
"""
import streamlit as st

# Import modules
from utils.config import setup_page, AZURE_API_KEY, AZURE_ENDPOINT, AZURE_DEPLOYMENT, AZURE_API_VERSION
from utils.kb_manager import load_knowledge_base, create_symptom_mapping, get_treatment_info
from utils.symptom_analyzer import find_diseases
from utils.llm_interface import initialize_azure_client, process_natural_language_symptoms, enhance_treatment_description
from utils.session_manager import initialize_session_state
import utils.ui_components as ui

def main():
    # Set up the page
    setup_page()
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize Azure OpenAI client
    client = initialize_azure_client(AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION)
    
    # Load knowledge base
    kb_data = load_knowledge_base()
    symptom_map, all_symptoms, disease_symptoms = create_symptom_mapping(kb_data)
    
    # Render UI header
    ui.render_header()
    
    # Render sidebar
    ui.render_sidebar(
        st.session_state.llm_mode, 
        client, 
        AZURE_DEPLOYMENT, 
        all_symptoms, 
        process_natural_language_symptoms
    )
    
    # Main content area
    if st.session_state.selected_symptoms:
        # Show analysis results
        ui.render_analysis_results()
    else:
        # Welcome screen
        ui.render_welcome_screen()
    
    # Display treatment information if a disease is selected
    if st.session_state.selected_disease:
        treatment_info = get_treatment_info(kb_data, st.session_state.selected_disease)
        
        if treatment_info:
            # Render treatment options
            ui.render_treatment_options(treatment_info, st.session_state.llm_mode, client, AZURE_DEPLOYMENT)
            
            # Display treatments based on selected view
            render_treatment_details(treatment_info, st.session_state.llm_mode, client, AZURE_DEPLOYMENT)
            
            
            # Back button
            if st.button("← Back to Disease List"):
                st.session_state.selected_disease = None
                st.session_state.treatment_view = None
                st.rerun()
    
    # Add AI chat section if LLM mode is enabled
    if st.session_state.llm_mode:
        render_ai_chat(client, AZURE_DEPLOYMENT)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p>Holistic Medicine Chatbot | Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

def render_treatment_details(treatment_info, llm_mode, client, deployment):
    """Render the details of treatments based on the view selection."""
    # Import the disclaimer module
    from utils.disclaimers import get_disclaimer, DISCLAIMER_CSS
    
    # Add the CSS for disclaimers once at the top
    st.markdown(DISCLAIMER_CSS, unsafe_allow_html=True)
    
    if st.session_state.treatment_view == "all" or st.session_state.treatment_view == "ayurvedic":
        # Get enhanced description if LLM mode is on
        if llm_mode and client:
            with st.spinner("Enhancing Ayurvedic treatment information..."):
                ayurvedic_treatment = enhance_treatment_description(
                    client,
                    deployment,
                    "Ayurvedic", 
                    treatment_info['Ayurvedic'],
                    st.session_state.selected_disease,
                    treatment_info['Symptoms']
                )
        else:
            ayurvedic_treatment = treatment_info['Ayurvedic']
            
        st.markdown("""
        <div class='treatment-card ayurvedic'>
            <h3 class='treatment-header'>🌿 Ayurvedic Treatment</h3>
            <p>{}</p>
        </div>
        """.format(ayurvedic_treatment), unsafe_allow_html=True)
        
        # Add the Ayurvedic-specific disclaimer
        st.markdown(get_disclaimer("Ayurvedic"), unsafe_allow_html=True)
        
    if st.session_state.treatment_view == "all" or st.session_state.treatment_view == "homeopathic":
        # Get enhanced description if LLM mode is on
        if llm_mode and client:
            with st.spinner("Enhancing Homeopathic treatment information..."):
                homeopathic_treatment = enhance_treatment_description(
                    client,
                    deployment,
                    "Homeopathic", 
                    treatment_info['Homeopathic'],
                    st.session_state.selected_disease,
                    treatment_info['Symptoms']
                )
        else:
            homeopathic_treatment = treatment_info['Homeopathic']
            
        st.markdown("""
        <div class='treatment-card homeopathic'>
            <h3 class='treatment-header'>💧 Homeopathic Treatment</h3>
            <p>{}</p>
        </div>
        """.format(homeopathic_treatment), unsafe_allow_html=True)
        
        # Add the Homeopathic-specific disclaimer
        st.markdown(get_disclaimer("Homeopathic"), unsafe_allow_html=True)
        
    if st.session_state.treatment_view == "all" or st.session_state.treatment_view == "allopathic":
        # Get enhanced description if LLM mode is on
        if llm_mode and client:
            with st.spinner("Enhancing Allopathic treatment information..."):
                allopathic_treatment = enhance_treatment_description(
                    client,
                    deployment,
                    "Allopathic", 
                    treatment_info['Allopathic'],
                    st.session_state.selected_disease,
                    treatment_info['Symptoms']
                )
        else:
            allopathic_treatment = treatment_info['Allopathic']
            
        st.markdown("""
        <div class='treatment-card allopathic'>
            <h3 class='treatment-header'>💊 Allopathic Treatment</h3>
            <p>{}</p>
        </div>
        """.format(allopathic_treatment), unsafe_allow_html=True)
        
        # Add the Allopathic-specific disclaimer
        st.markdown(get_disclaimer("Allopathic"), unsafe_allow_html=True)
    
    # If showing all treatments, add the general disclaimer at the bottom
    if st.session_state.treatment_view == "all":
        st.markdown("---")
        st.markdown(get_disclaimer("General"), unsafe_allow_html=True)

def render_ai_chat(client, deployment):
    """Render the AI chat section for follow-up questions."""
    from utils.llm_interface import get_llm_response
    from utils.kb_manager import get_treatment_info
    from utils.session_manager import add_to_chat_history
    
    st.markdown("---")
    st.header("💬 AI Health Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: #e3f0ff; padding: 10px; border-radius: 10px; margin-bottom: 10px;'><strong>Assistant:</strong> {message['content']}</div>", unsafe_allow_html=True)
    
    # Chat input
    user_question = st.text_input("Ask a question about your condition, treatments, or health:", key="chat_input")
    
    if user_question and st.button("Ask Assistant"):
        # Add user message to chat history
        add_to_chat_history("user", user_question)
        
        # Create context from session state
        context = ""
        if st.session_state.selected_symptoms:
            context += f"User Symptoms: {', '.join(st.session_state.selected_symptoms)}\n"
        
        if st.session_state.selected_disease:
            kb_data = load_knowledge_base()
            context += f"Currently Viewing: {st.session_state.selected_disease}\n"
            treatment_info = get_treatment_info(kb_data, st.session_state.selected_disease)
            if treatment_info:
                context += f"Category: {treatment_info['Category']}\n"
                context += f"Symptoms: {treatment_info['Symptoms']}\n"
                context += f"Ayurvedic Treatment: {treatment_info['Ayurvedic']}\n"
                context += f"Homeopathic Treatment: {treatment_info['Homeopathic']}\n"
                context += f"Allopathic Treatment: {treatment_info['Allopathic']}\n"
        
        # Generate AI response
        with st.spinner("Generating response..."):
            prompt = f"""
            You are a knowledgeable health assistant specializing in holistic medicine. Use the following context to answer the user's question.
            Provide helpful, accurate information while maintaining appropriate medical disclaimers.
            
            Context:
            {context}
            
            User's question: {user_question}
            
            Provide a clear, informative response. If you don't have enough information or if the question is beyond your capabilities,
            suggest that the user consult with a healthcare professional.
            """
            
            ai_response = get_llm_response(client, deployment, prompt)
            add_to_chat_history("assistant", ai_response)
        
        # Force a rerun to display the new messages
        st.rerun()

if __name__ == "__main__":
    main()
