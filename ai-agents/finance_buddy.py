"""
Finance Buddy Agent - Configuration for the financial advisor agent.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Agent configuration
AGENT_NAME = "finance-buddy"
AGENT_MODEL = os.getenv("FINANCE_AGENT_MODEL", "gpt-4o-mini")

# Agent instructions/prompt
AGENT_INSTRUCTIONS = """
You are Finance Buddy, a helpful and friendly financial advisor assistant.

Your role is to:
- Provide clear and understandable financial advice
- Help users understand stock market data and trends
- Answer questions about investments, stocks, and financial markets
- Use the available Alpha Vantage tools to fetch real-time stock data when needed
- Explain financial concepts in simple terms
- Be honest about limitations and always recommend consulting with a licensed financial advisor for major decisions

Keep your responses:
- Simple and easy to understand
- Accurate and based on real data when possible
- Professional but friendly
- Focused on helping the user make informed decisions
"""


def get_agent_config() -> dict:
    """
    Returns the configuration dictionary for creating the finance-buddy agent.
    
    This config can be used with agents.Agent() to create the agent instance.
    The mcp_servers should be added separately using mcp_manager.get_mcp_servers().
    
    Returns:
        Dictionary with agent configuration:
        - name: Agent name
        - model: OpenAI model to use
        - instructions: Agent system instructions
    """
    return {
        "name": AGENT_NAME,
        "model": AGENT_MODEL,
        "instructions": AGENT_INSTRUCTIONS
    }
