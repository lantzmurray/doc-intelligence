from .base import call_llm, log_agent_response, get_topic_log
from typing import Dict, Any
import logging


# Configure logging for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



"""
Summary Agent - Condenses document content into bullet summaries
For Document Intelligence Workspace
"""

def run(topic: str, model: str = "llama2", bullet_points: int = 5) -> Dict[str, Any]:
    """
    Run summary agent to condense document content
    
    Args:
        topic: Document name
        model: LLM model to use
        bullet_points: Number of bullet points to generate
    
    Returns:
        Dictionary with summary response
    """
    # Get all accumulated knowledge from shared memory
    memory = get_topic_log(topic)
    
    if not memory:
        return {
            "agent": "Summary Agent",
            "topic": topic,
            "response": "No document content to summarize yet. Please upload a document first.",
            "status": "no_data"
        }
    
    # Build memory context from all agent contributions
    memory_context = "\n".join([
        f"{entry['agent']}: {entry['content']}" 
        for entry in memory
    ])
    
    prompt = f"""
Summarize the following document into {bullet_points} concise, actionable bullet points.

Document Content:
{memory_context}

Focus on:
1. Key findings and insights
2. Important themes and patterns
3. Critical information
4. Actionable takeaways

Format each bullet point with a clear heading followed by a brief explanation.
"""
    
    summary = call_llm(prompt, model)
    log_agent_response(topic, "Summary Agent", summary)
    
    return {
        "agent": "Summary Agent",
        "topic": topic,
        "response": summary,
        "bullet_points": bullet_points,
        "status": "success"
    }


def run_comprehensive_summary(topic: str, model: str = "llama2") -> Dict[str, Any]:
    """
    Run comprehensive summary with multiple sections
    
    Args:
        topic: Document name
        model: LLM model to use
    
    Returns:
        Dictionary with comprehensive summary response
    """
    memory = get_topic_log(topic)
    
    if not memory:
        return {
            "agent": "Summary Agent",
            "topic": topic,
            "response": "No document content to summarize yet. Please upload a document first.",
            "status": "no_data"
        }
    
    memory_context = "\n".join([
        f"{entry['agent']}: {entry['content']}" 
        for entry in memory
    ])
    
    prompt = f"""
Create a comprehensive summary of the following document.

Document Content:
{memory_context}

Structure the summary with these sections:
1. Executive Summary (2-3 paragraphs)
2. Key Findings (5-7 bullet points)
3. Main Themes (3-5 themes)
4. Critical Insights (3-5 insights)

Use clear headings and professional language.
"""
    
    summary = call_llm(prompt, model)
    log_agent_response(topic, "Summary Agent", summary)
    
    return {
        "agent": "Summary Agent",
        "topic": topic,
        "response": summary,
        "summary_type": "comprehensive",
        "status": "success"
    }


def run_agent_summary(topic: str, agent_name: str, model: str = "llama2") -> Dict[str, Any]:
    """
    Summarize contributions from a specific agent
    
    Args:
        topic: Research topic
        agent_name: Name of agent to summarize
        model: LLM model to use
    
    Returns:
        Dictionary with agent-specific summary
    """
    from .base import get_agent_contributions
    
    contributions = get_agent_contributions(topic, agent_name)
    
    if not contributions:
        return {
            "agent": "Summarizer Agent",
            "topic": topic,
            "target_agent": agent_name,
            "response": f"No contributions found from {agent_name} yet.",
            "status": "no_data"
        }
    
    contributions_text = "\n".join([
        c["content"] for c in contributions
    ])
    
    prompt = f"""
Summarize the following contributions from {agent_name}:

Contributions:
{contributions_text}

Provide:
1. Key points and insights
2. Main themes
3. Important findings

Format as a clear, structured summary.
"""
    
    summary = call_llm(prompt, model)
    
    return {
        "agent": "Summarizer Agent",
        "topic": topic,
        "target_agent": agent_name,
        "response": summary,
        "status": "success"
    }
