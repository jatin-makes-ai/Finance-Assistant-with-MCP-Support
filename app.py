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

def extract_text(content):
    """Extract text from Gradio content which can be a string or dict/list."""
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", str(content))
    elif isinstance(content, list) and len(content) > 0:
        return extract_text(content[0])
    return str(content)

async def chat_handler(message, history):
    """Gradio handler that ensures a stable connection."""
    try:
        # Get agent in the current loop
        agent = await get_or_create_agent()
        
        # Build conversation context as a simple string
        # This is simpler and more reliable than complex message formatting
        context = ""
        for item in history:
            if isinstance(item, dict):
                # Gradio 5+ "messages" format
                role = item["role"]
                content = extract_text(item["content"])
                if role == "user":
                    context += f"User: {content}\n"
                else:
                    context += f"Assistant: {content}\n"
            else:
                # Gradio 4- "tuples" format (user_msg, bot_msg)
                user_msg, bot_msg = item
                context += f"User: {user_msg}\n"
                context += f"Assistant: {bot_msg}\n"
        
        # Add current message
        full_input = context + f"User: {message}\n"
        
        # Run the agent with simple string input
        result = await Runner.run(agent, full_input.strip())
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