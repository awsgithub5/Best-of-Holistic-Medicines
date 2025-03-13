# Holistic Medicine Chatbot

A Streamlit application that provides treatment suggestions from Ayurvedic, Homeopathic, and Allopathic medicine systems based on user symptoms.

## Features

- Input symptoms through text or quick selection buttons
- Symptom suggestion functionality as you type
- Analysis of symptoms to find potential matching conditions
- Detailed treatment recommendations from three medical approaches:
  - Ayurvedic Medicine
  - Homeopathic Medicine
  - Allopathic Medicine
- Knowledge base of 84 common diseases and conditions

## Installation

1. Clone this repository
2. Install the required packages:

```bash
pip install streamlit
```

3. Make sure to place the `kb.json` knowledge base file in the same directory as the app.py file.

## Running the App

Navigate to the directory containing the app and run:

```bash
streamlit run app.py
```

## How to Use

1. Enter your symptoms using the text input or quick selection buttons in the sidebar
2. Click "Analyze Symptoms" to get potential conditions
3. Select a condition to view treatment options
4. Choose which medicine system(s) you'd like to see treatments from

## Knowledge Base

The app uses a knowledge base of 84 diseases covering:
- Respiratory conditions
- Cardiovascular diseases
- Digestive disorders
- Neurological conditions
- Psychological disorders
- Musculoskeletal issues
- Dermatological problems
- Infectious diseases
- Developmental conditions
- And more

## Disclaimer

This application is for educational purposes only and is not intended to replace professional medical advice. Always consult a healthcare professional for proper diagnosis and treatment.

# Key Features

User-Friendly Interface: Clean design with intuitive navigation
Smart Symptom Suggestions: As users type, the app suggests matching symptoms
Comprehensive Knowledge Base: Uses your database of 84 diseases covering multiple categories
Symptom Matching Algorithm: Calculates match scores based on symptom overlap
Multi-Treatment View: Users can view all approaches or filter by specific medical system
Responsive Design: Works well on both desktop and mobile devices

## Future Enhancements

- Adding more diseases to the knowledge base
- Improving symptom matching algorithm
- Incorporating medical images for visual reference
- Adding preventative measures for each condition



# ******************************************************************************

# I've created a complete application that uses a pre-existing knowledge base without requiring real-time LLM inferencing.
# Here's what's happening in the application:

# Knowledge Base Utilization
The app loads and processes your existing knowledge base (kb.json) that contains 84 diseases with their symptoms and treatments across the three medical systems.

# Symptom Matching Algorithm: 
I've implemented a custom symptom matching algorithm that:
Maps symptoms to potential diseases
Calculates match scores based on how many of the user's symptoms match with each disease
Ranks the potential diseases by this score


# No Real-time LLM Required: 
The implementation doesn't need a GPT-4o or other LLM during runtime. All the logic is handled by the Python code and the pre-loaded knowledge base, making it:

# Faster (no API calls)
More economical (no token usage)
More predictable (deterministic responses)


# Focused Functionality: 
Instead of using an LLM for general-purpose chat, the app is specifically designed to:
Accept symptoms
Match them to conditions
Present structured treatment options


# *******************************************************************************

# Holistic Medicine Chatbot with LLM Enhancement
I've enhanced the holistic medicine chatbot by integrating LLM capabilities for more natural interaction and richer content. Here's what's new:
Key LLM Enhancements

# Natural Language Symptom Processing
Users can now describe how they feel in everyday language
The LLM extracts specific symptoms from natural descriptions
Example: "I've been feeling dizzy and nauseous since yesterday" → extracts "dizziness, nausea"


# Enhanced Treatment Explanations

# When the AI mode is enabled, treatment descriptions are enhanced with:
More detailed explanations of remedies
Potential benefits and considerations
More accessible language and context


# AI Health Assistant Chat

Users can ask follow-up questions about their conditions or treatments
The chat maintains context of the user's symptoms and selected conditions
Provides personalized health information while maintaining appropriate medical disclaimers



# Implementation Details

Toggle for AI Mode: Users can switch between basic mode and AI-enhanced mode
OpenAI Integration: Uses the OpenAI API (with GPT-4o recommended)
Environment Variables: API key configured via .env file or environment variables
Graceful Fallbacks: The app still functions without an API key, just with reduced capabilities


# *********************************************************************************

# Testing the Enhanced Features

Enable AI mode with the toggle in the sidebar
Try describing symptoms in natural language:

"I've been having headaches and dizziness for the past few days"
"My joints hurt when I wake up and the pain gets better during the day"


Select a condition to view AI-enhanced treatment explanations
Use the AI chat section to ask follow-up questions:

"What lifestyle changes would help with this condition?"
"Are there any foods I should avoid?"
"How long does it typically take for these treatments to work?"