import streamlit as st
import os
import sys

# Add the parent directory to sys.path so we can import from the orchestrator and utils
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(PROJECT_ROOT))
sys.path.append(PROJECT_ROOT)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

# Import the orchestrator workflow function
# This function handles extracting text and running all the agents
from orchestrator import process_document_workflow
from components import render_app_footer, run_with_status_updates

# Configure the page title and layout
st.set_page_config(page_title="Document Intelligence Workspace", layout="wide")

# Set up the main title and description for the Streamlit web app
st.title("Document Intelligence Workspace")
st.write("Upload a document and let our AI agents collaboratively analyze it.")

# Create an uploads directory to store temporary files if it doesn't exist
# This is where we save files before passing them to the document parser
os.makedirs("uploads", exist_ok=True)

# Provide a file uploader widget in the UI
# We accept PDF, DOCX, and TXT files as supported by our document_parser.py
uploaded_file = st.file_uploader("Upload document", type=["pdf", "docx", "txt"])

# If the user has successfully uploaded a file
if uploaded_file:
    # Define the local path where the file will be saved temporarily
    file_path = f"uploads/{uploaded_file.name}"
    
    # Open the file in write-binary mode ("wb") and save the uploaded buffer
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Provide a button to trigger the analysis workflow
    if st.button("Start Collaborative Analysis"):
        # Keep the UI visibly alive while the agents are working.
        results = run_with_status_updates(
            lambda: process_document_workflow(file_path, uploaded_file.name),
            start_message="Agents are collaboratively analyzing the document..."
        )
            
        # Display the Summary Agent's results
        st.subheader("📝 Summary Agent")
        st.write(results.get("summary", "No summary provided."))
        
        # Add a visual separator
        st.divider()
        
        # Display the Red Flag Detector's results
        st.subheader("🚩 Red Flag Detector")
        st.write(results.get("red_flags", "No red flags found."))
        
        # Add another visual separator
        st.divider()
        
        # Display the Decision Extractor's results
        st.subheader("✅ Decision Extractor")
        st.write(results.get("decisions", "No decisions extracted."))


render_app_footer()
