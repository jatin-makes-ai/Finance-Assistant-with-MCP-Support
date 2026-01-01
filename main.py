"""
Main script for Finance Buddy agent with proper async MCP server connection.
"""
import asyncio
import logging
import sys
from pathlib import Path

# --- 1. CONFIGURATION & SETUP ---
# Configure root logger first to capture everything
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

# SILENCE NOISY LOGGERS (Critical Step)
# This stops the "HTTP Request: POST..." and "Received session ID..." spam
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("httpcore").setLevel(logging.ERROR)
logging.getLogger("mcp").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("openai").setLevel(logging.ERROR)

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent / "ai-agents"))

# Import your modules
from agents import Agent, Runner
from finance_buddy import get_agent_config
from mcp_manager import get_mcp_servers

logger = logging.getLogger("FinanceBuddy")

# --- 2. CORE LOGIC ---

async def main_async():
    """
    Main execution logic using Connect -> Run -> Disconnect pattern.
    """
    logger.info("Initializing Agent...")
    
    # Setup
    config = get_agent_config()
    mcp_servers = get_mcp_servers()
    
    agent = Agent(
        name=config["name"],
        instructions=config["instructions"],
        model=config["model"],
        mcp_servers=mcp_servers
    )

    try:
        # Connect
        if mcp_servers:
            logger.info(f"Connecting to {len(mcp_servers)} MCP server(s)...")
            for server in mcp_servers:
                await server.connect()
            logger.info("MCP servers connected.")

        # Run Query
        query = "What is the price of the AAPL stock presently?"
        logger.info(f"Processing query: {query}")
        
        # Run agent
        result = await Runner.run(agent, query)
        
        # Output
        print("\n" + "="*50)
        print("FINAL RESPONSE:")
        print(result.final_output)
        print("="*50 + "\n")

    except Exception as e:
        logger.error(f"Execution failed: {e}")

    finally:
        # Cleanup
        if mcp_servers:
            logger.info("Closing MCP connections...")
            for server in mcp_servers:
                try:
                    # Disconnect attempts to close the session
                    await server.disconnect()
                except Exception:
                    pass
            
            # TRICK: Give the background HTTP client a moment to finish 
            # the DELETE request before we kill the event loop.
            await asyncio.sleep(0.5) 
            logger.info("Connections closed.")

# --- 3. ENTRY POINT ---

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass
    except RuntimeError as e:
        # Suppress the known AnyIO/MCP shutdown noise
        if "Attempted to exit cancel scope" in str(e):
            pass 
        else:
            raise e

if __name__ == "__main__":
    main()