from .base import call_llm, log_agent_response, get_topic_log
from typing import Dict, Any
import logging


# Configure logging for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



"""
Red Flag Detector - Challenges assumptions and raises counterpoints
For Document Intelligence Workspace
"""

def run(topic: str, model: str = "llama2", focus: str = "standard") -> Dict[str, Any]:
    """
    Run Red Flag Detector to challenge accumulated knowledge
    
    Args:
        topic: Document name
        model: LLM model to use
        focus: Focus area (standard, risk, scenarios)
    
    Returns:
        Dictionary with agent response
    """
    # Get all accumulated knowledge from shared memory
    memory = get_topic_log(topic)
    
    if not memory:
        return {
            "agent": "Red Flag Detector",
            "topic": topic,
            "response": "No document content to analyze yet. Please upload a document first.",
            "status": "no_data"
        }
    
    # Build memory context from all agent contributions
    memory_context = "\n".join([
        f"{entry['agent']}: {entry['content']}" 
        for entry in memory
    ])
    
    prompt = ""
    if focus == "risk":
        prompt = f"""
Act as a Red Flag Detector for the following document.

Document Content:
{memory_context}

Identify any risks, liabilities, compliance issues, or problematic clauses. Focus strictly on potential negative consequences.
"""
    elif focus == "scenarios":
        prompt = f"""
Act as a Red Flag Detector for the following document.

Document Content:
{memory_context}

Generate alternative scenarios where the terms, statements, or assumptions in this document could fail or be exploited.
"""
    else:
        prompt = f"""
Act as a Red Flag Detector for the following document.

Document Content:
{memory_context}

Review the document and identify any red flags, hidden obligations, or areas that require critical scrutiny.
"""
    
    challenges = call_llm(prompt, model)
    log_agent_response(topic, "Red Flag Detector", challenges)
    
    return {
        "agent": "Red Flag Detector",
        "topic": topic,
        "response": challenges,
        "focus": focus,
        "status": "success"
    }
