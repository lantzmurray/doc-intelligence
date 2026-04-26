import os
# Import the document parsing utility to extract text from files (PDF, DOCX, TXT)
from utils.document_parser import extract_text

# Import the run functions from our specialized agents
import agents.summary_agent as summary_agent
import agents.red_flag_detector as red_flag_detector
import agents.decision_extractor as decision_extractor

# Import the base agent functionality to log the initial document to memory
from agents.base import log_agent_response, db, delete_topic

def process_document_workflow(file_path: str, filename: str, model: str = "llama2"):
    """
    Extract text from an uploaded document and run the collaborative multi-agent workflow.
    
    This function mimics the shared memory approach from Project 13:
    1. It extracts text from the document.
    2. It saves the text into the shared TinyDB memory using the filename as the "topic".
    3. It runs the three specialized agents sequentially, allowing them to read from memory.
    4. It returns the aggregated results to the frontend.
    
    Args:
        file_path (str): The local path where the uploaded file is temporarily saved.
        filename (str): The name of the file (used as the unique 'topic' in memory).
        model (str): The LLM model to use for the agents (default: "llama2").
        
    Returns:
        dict: A dictionary containing the responses from the three agents.
    """
    # 1. Extract the text from the uploaded document file
    extracted_data = extract_text(file_path)
    # Fallback to an empty string if the text couldn't be extracted
    text = extracted_data.get("text", "")
    
    if not text.strip():
        # Return a warning if the file was empty or unreadable
        return {
            "summary": "Could not extract text from the document. It might be empty or in an unsupported format.",
            "red_flags": "N/A",
            "decisions": "N/A"
        }
    
    # Optional: Clear any previous analysis for this same filename so we start fresh
    # This prevents the memory from growing indefinitely if the user uploads the same file twice
    delete_topic(filename)
    
    # 2. Store the initial document text into shared memory
    # We use the 'filename' as the 'topic' identifier in our TinyDB
    # We log it under a generic "Document Parser" agent name
    log_agent_response(topic=filename, agent="Document Parser", content=text)
    
    # 3. Run the Summary Agent
    # The agent will look up the 'filename' topic in memory, read the document text, and summarize it.
    summary_result = summary_agent.run(topic=filename, model=model)
    
    # 4. Run the Red Flag Detector
    # The agent will read the document from memory and identify potential risks and liabilities.
    red_flag_result = red_flag_detector.run(topic=filename, model=model)
    
    # 5. Run the Decision Extractor
    # The agent will read the document and extract key decisions and explicit obligations.
    decision_result = decision_extractor.run(topic=filename, model=model)
    
    # 6. Aggregate the results and return them to the frontend for display
    # The .get("response", "") ensures we return a string even if the agent failed or returned an unexpected format
    return {
        "summary": summary_result.get("response", "Error: Summary Agent failed to respond."),
        "red_flags": red_flag_result.get("response", "Error: Red Flag Detector failed to respond."),
        "decisions": decision_result.get("response", "Error: Decision Extractor failed to respond.")
    }
