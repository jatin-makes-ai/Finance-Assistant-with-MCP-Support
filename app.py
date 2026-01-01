import asyncio
import logging
import gradio as gr
import sys
from pathlib import Path

# Silence the noise
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
for logger_name in ["httpx", "httpcore", "mcp", "openai", "anyio"]:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

sys.path.insert(0, str(Path(__file__).parent / "ai-agents"))
from agents import Runner, Agent
from finance_buddy import get_agent_config
from mcp_manager import get_mcp_servers

# Global state
class AppState:
    agent = None
    servers = []

state = AppState()

async def get_or_create_agent():
    """Ensures agent is connected within the current running event loop."""
    if state.agent is not None:
        return state.agent

    print("🚀 Connecting to MCP Servers...")
    config = get_agent_config()
    state.servers = get_mcp_servers()
    
    state.agent = Agent(
        name=config["name"],
        instructions=config["instructions"],
        model=config["model"],
        mcp_servers=state.servers
    )
    
    for server in state.servers:
        await server.connect()
    
    print("✅ System Ready.")
    return state.agent

async def chat_handler(message, history):
    """Gradio handler that ensures a stable connection."""
    try:
        # Get agent in the current loop
        agent = await get_or_create_agent()
        
        # Run the agent - Note: We skip the 'trace' wrapper to avoid the 400 error
        result = await Runner.run(agent, message)
        return result.final_output
    
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Define UI
with gr.Blocks(title="Finance Buddy") as demo:
    gr.Markdown("# 💸 Finance Assistant")
    gr.ChatInterface(
        fn=chat_handler,
        # type="messages",
    )

if __name__ == "__main__":
    # Gradio 5.0+ manages the event loop for us
    # We don't call asyncio.run() here; demo.launch() handles it
    demo.launch()