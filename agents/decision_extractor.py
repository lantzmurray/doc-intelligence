from .base import call_llm, log_agent_response, get_topic_log
from typing import Dict, Any
import logging


# Configure logging for this module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



"""
Decision Extractor - Extracts key decisions, obligations, and actionable items
For Document Intelligence Workspace
"""

def run(topic: str, model: str = "llama2") -> Dict[str, Any]:
    """
    Run Decision Extractor to extract key decisions
    
    Args:
        topic: Document name
        model: LLM model to use
    
    Returns:
        Dictionary with extracted decisions
    """
    # Get accumulated knowledge from shared memory
    memory = get_topic_log(topic)
    
    if not memory:
        return {
            "agent": "Decision Extractor",
            "topic": topic,
            "response": "No document content to extract decisions from yet. Please upload a document first.",
            "status": "no_data"
        }
    
    # Build memory context from all agent contributions
    memory_context = "\n".join([
        f"{entry['agent']}: {entry['content']}" 
        for entry in memory
    ])
    
    prompt = f"""
Extract all key decisions, obligations, and actionable items from the following document.

Document Content:
{memory_context}

Provide:
1. Key decisions made or stated
2. Explicit obligations (who must do what)
3. Actionable next steps or requirements
4. Important dates or deadlines mentioned

Format each point clearly with supporting context.
"""
    
    decisions = call_llm(prompt, model)
    log_agent_response(topic, "Decision Extractor", decisions)
    
    return {
        "agent": "Decision Extractor",
        "topic": topic,
        "response": decisions,
        "status": "success"
    }


def run_strategic_analysis(topic: str, model: str = "llama2") -> Dict[str, Any]:
    """
    Run strategic analysis focused on implications
    
    Args:
        topic: Research topic
        model: LLM model to use
    
    Returns:
        Dictionary with strategic analysis response
    """
    memory = get_topic_log(topic)
    
    if not memory:
        return {
            "agent": "Insight Agent",
            "topic": topic,
            "response": "No accumulated knowledge to analyze strategically yet. Run other agents first.",
            "status": "no_data"
        }
    
    memory_context = "\n".join([
        f"{entry['agent']}: {entry['content']}" 
        for entry in memory
    ])
    
    prompt = f"""
Conduct a strategic analysis of the following accumulated research.

Accumulated Research:
{memory_context}

Analyze and provide:
1. Strategic implications (short-term and long-term)
2. Market opportunities
3. Competitive landscape insights
4. Investment priorities
5. Risk-return assessment
6. Recommended strategic actions

Use strategic thinking frameworks and business language.
"""
    
    strategic_analysis = call_llm(prompt, model)
    log_agent_response(topic, "Insight Agent", strategic_analysis)
    
    return {
        "agent": "Insight Agent",
        "topic": topic,
        "response": strategic_analysis,
        "analysis_type": "strategic",
        "status": "success"
    }


def run_trend_analysis(topic: str, model: str = "llama2") -> Dict[str, Any]:
    """
    Run trend analysis to identify patterns
    
    Args:
        topic: Research topic
        model: LLM model to use
    
    Returns:
        Dictionary with trend analysis response
    """
    memory = get_topic_log(topic)
    
    if not memory:
        return {
            "agent": "Insight Agent",
            "topic": topic,
            "response": "No accumulated knowledge to analyze trends for yet. Run other agents first.",
            "status": "no_data"
        }
    
    memory_context = "\n".join([
        f"{entry['agent']}: {entry['content']}" 
        for entry in memory
    ])
    
    prompt = f"""
Analyze the following accumulated research for trends and patterns.

Accumulated Research:
{memory_context}

Identify and analyze:
1. Emerging trends
2. Converging themes
3. Diverging viewpoints
4. Temporal patterns (if applicable)
5. Causal relationships
6. Predictive indicators

For each trend, provide:
- Description
- Evidence from research
- Implications
- Confidence level

Help identify what's driving change and what might happen next.
"""
    
    trend_analysis = call_llm(prompt, model)
    log_agent_response(topic, "Insight Agent", trend_analysis)
    
    return {
        "agent": "Insight Agent",
        "topic": topic,
        "response": trend_analysis,
        "analysis_type": "trends",
        "status": "success"
    }
