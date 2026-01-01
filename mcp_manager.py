"""
MCP Manager - Handles MCP server configuration and creation from mcp.json
"""

import json
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams


def load_mcp_config(config_path: Optional[str] = None) -> dict:
    """
    Load MCP configuration from mcp.json file.
    
    Args:
        config_path: Path to mcp.json file. If None, looks for mcp.json in project root.
    
    Returns:
        Dictionary containing MCP server configurations
    """
    if config_path is None:
        config_path = Path(__file__).parent / "mcp.json"
    else:
        config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"MCP configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def create_mcp_servers(config_path: Optional[str] = None) -> List[MCPServerStreamableHttp]:
    """
    Create MCP server instances from mcp.json configuration.
    
    Args:
        config_path: Path to mcp.json file. If None, looks for mcp.json in project root.
    
    Returns:
        List of MCPServerStreamableHttp instances
    """
    config = load_mcp_config(config_path)
    mcp_servers = []
    
    servers_config = config.get("servers", {})
    
    for server_name, server_config in servers_config.items():
        server_type = server_config.get("type", "").lower()
        
        if server_type == "http":
            # HTTP/Streamable HTTP server
            url = server_config.get("url", "")
            
            # Replace placeholder API keys with environment variables
            if "YOUR_API_KEY" in url:
                # Try to get API key from environment
                if "alphavantage" in server_name.lower():
                    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "")
                    if api_key:
                        url = url.replace("YOUR_API_KEY", api_key)
                    else:
                        continue  # Skip if API key not available
                else:
                    # For other servers, try generic API key env var
                    api_key = os.getenv(f"{server_name.upper()}_API_KEY", "")
                    if api_key:
                        url = url.replace("YOUR_API_KEY", api_key)
                    else:
                        continue
            
            if url:
                mcp_server = MCPServerStreamableHttp(
                    params=MCPServerStreamableHttpParams(url=url)
                )
                mcp_servers.append(mcp_server)
        
        # Note: stdio servers are not supported in this implementation
        # as they require different handling
    
    return mcp_servers


def get_mcp_servers() -> List[MCPServerStreamableHttp]:
    """
    Convenience function to get MCP servers from default mcp.json location.
    
    Returns:
        List of MCPServerStreamableHttp instances
    """
    return create_mcp_servers()

