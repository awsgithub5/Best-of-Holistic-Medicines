
"""
Interactive body map for symptom selection in the holistic medicine chatbot.
"""
import streamlit as st

def render_body_map():
    """
    Render an interactive SVG body map for symptom selection.
    """
    st.subheader("Select Area of Symptoms")
    
    # SVG body map with clickable regions
    svg_html = """
    <style>
        .body-map {
            display: block;
            margin: 0 auto;
            width: 100%;
            max-width: 400px;
        }
        .body-part {
            fill: #e0e0e0;
            stroke: #333;
            stroke-width: 1;
            transition: fill 0.3s;
            cursor: pointer;
        }
        .body-part:hover {
            fill: #a8d5ff;
        }
        .selected {
            fill: #4a89dc !important;
        }
    </style>
    
    <svg class="body-map" viewBox="0 0 200 400" xmlns="http://www.w3.org/2000/svg">
        <g id="body-map-parts">
            <!-- Head -->
            <circle id="head" class="body-part" cx="100" cy="40" r="30" 
                onclick="selectBodyPart('head', 'Headache, Migraine, Dizziness')" />
            
            <!-- Chest -->
            <rect id="chest" class="body-part" x="70" y="80" width="60" height="60" 
                onclick="selectBodyPart('chest', 'Chest pain, Cough, Shortness of breath')" />
            
            <!-- Abdomen -->
            <rect id="abdomen" class="body-part" x="70" y="145" width="60" height="50" 
                onclick="selectBodyPart('abdomen', 'Abdominal pain, Nausea, Bloating')" />
            
            <!-- Left Arm -->
            <rect id="left-arm" class="body-part" x="40" y="85" width="25" height="90" rx="10" 
                onclick="selectBodyPart('left-arm', 'Arm pain, Weakness, Joint pain')" />
            
            <!-- Right Arm -->
            <rect id="right-arm" class="body-part" x="135" y="85" width="25" height="90" rx="10" 
                onclick="selectBodyPart('right-arm', 'Arm pain, Weakness, Joint pain')" />
            
            <!-- Left Leg -->
            <rect id="left-leg" class="body-part" x="70" y="200" width="25" height="150" rx="10" 
                onclick="selectBodyPart('left-leg', 'Leg pain, Swelling, Joint pain')" />
            
            <!-- Right Leg -->
            <rect id="right-leg" class="body-part" x="105" y="200" width="25" height="150" rx="10" 
                onclick="selectBodyPart('right-leg', 'Leg pain, Swelling, Joint pain')" />
            
            <!-- Throat -->
            <rect id="throat" class="body-part" x="85" y="70" width="30" height="15" 
                onclick="selectBodyPart('throat', 'Sore throat, Difficulty swallowing')" />
            
            <!-- Back (behind figure) -->
            <rect id="back" class="body-part" x="170" y="110" width="20" height="80" 
                onclick="selectBodyPart('back', 'Back pain, Spinal issues')" />
            <text x="190" y="150" text-anchor="middle" transform="rotate(90, 190, 150)">Back</text>
        </g>
    </svg>
    
    <script>
        function selectBodyPart(part, symptoms) {
            // Remove current selections
            const parts = document.getElementsByClassName('body-part');
            for (let i = 0; i < parts.length; i++) {
                if (parts[i].id !== part) {
                    parts[i].classList.remove('selected');
                }
            }
            
            // Toggle selection on clicked part
            const element = document.getElementById(part);
            element.classList.toggle('selected');
            
            // Send the data to Streamlit
            const data = {
                part: part,
                selected: element.classList.contains('selected'),
                symptoms: symptoms
            };
            
            // Use Streamlit's setComponentValue to pass data back to Python
            if (data.selected) {
                window.parent.postMessage({
                    type: "streamlit:setComponentValue",
                    value: data
                }, "*");
            }
        }
    </script>
    """
    
    # Create a component for the body map
    component_value = st.components.v1.html(svg_html, height=500)
    
    # Process the selected body part
    if component_value:
        part = component_value.get("part")
        symptoms = component_value.get("symptoms")
        if part and symptoms:
            st.session_state.body_part = part
            st.session_state.suggested_symptoms = symptoms.split(", ")
            
            # Display suggested symptoms for selection
            st.subheader(f"Suggested symptoms for {part.replace('-', ' ').title()}")
            for symptom in st.session_state.suggested_symptoms:
                if st.button(symptom, key=f"body_map_{symptom}"):
                    if symptom not in st.session_state.selected_symptoms:
                        st.session_state.selected_symptoms.append(symptom)
                        st.experimental_rerun()

def initialize_body_map_state():
    """Initialize body map related session state variables."""
    if 'body_part' not in st.session_state:
        st.session_state.body_part = None
    if 'suggested_symptoms' not in st.session_state:
        st.session_state.suggested_symptoms = []