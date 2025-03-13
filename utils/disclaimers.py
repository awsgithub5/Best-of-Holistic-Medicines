# disclaimers.py
"""
Module for treatment-specific disclaimers to be displayed alongside treatment recommendations.
"""

# Disclaimers for each treatment type
DISCLAIMERS = {
    "Ayurvedic": """
    <div class="disclaimer-box">
        <p><strong>Note:</strong> These are general suggestions based on traditional Ayurvedic practices. 
        The severity and duration of your symptoms matter, and if they persist or worsen, 
        you should consult with a qualified healthcare professional or an Ayurvedic practitioner for personalized advice.</p>
    </div>
    """,
    
    "Homeopathic": """
    <div class="disclaimer-box">
        <p><strong>Note:</strong> These are general suggestions based on homeopathic principles. 
        Homeopathic remedies are highly individualized, and their effectiveness may vary. 
        If symptoms persist or worsen, please consult with a qualified homeopathic practitioner for a personalized treatment plan.</p>
    </div>
    """,
    
    "Allopathic": """
    <div class="disclaimer-box">
        <p><strong>Note:</strong> These are common over-the-counter recommendations. 
        For proper diagnosis and treatment, especially if symptoms are severe or persistent, 
        please consult with a qualified healthcare professional. Never self-medicate with prescription drugs.</p>
    </div>
    """,
    
    # "General": """
    # <div class="disclaimer-box">
    #     <p><strong>Disclaimer:</strong> The information provided is for educational purposes only and is not intended to be a substitute 
    #     for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified 
    #     health provider with any questions you may have regarding a medical condition.</p>
    # </div>
    # """
}

def get_disclaimer(treatment_type):
    """
    Returns the appropriate disclaimer for a specific treatment type.
    
    Args:
        treatment_type (str): The type of treatment ("Ayurvedic", "Homeopathic", or "Allopathic")
        
    Returns:
        str: HTML-formatted disclaimer text
    """
    return DISCLAIMERS.get(treatment_type)

# Additional CSS for styling the disclaimers
DISCLAIMER_CSS = """
<style>
    .disclaimer-box {
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
        padding: 10px 15px;
        margin: 10px 0;
        font-size: 0.9rem;
        border-radius: 4px;
    }
    .disclaimer-box p {
        margin: 0;
        color: #495057;
    }
</style>
"""