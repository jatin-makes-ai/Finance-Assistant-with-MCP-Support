# Finance Buddy - Financial Advisor Agent

A simple and understandable financial advisor application using OpenAI Agents SDK with MCP integration for Alpha Vantage tools.

## Project Structure

```
Financial-Advisor/
├── ai-agents/
│   └── finance-buddy.py    # Agent configuration and setup
├── app.py                   # Gradio chat interface
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

You can set environment variables in two ways:

#### Option 1: Using a `.env` file (Recommended)

Create a `.env` file in the project root directory with the following content:

```env
OPENAI_API_KEY=your-openai-api-key-here
FINANCE_AGENT_MODEL=gpt-4o-mini
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key-here
```

**Note:** Make sure to add `.env` to your `.gitignore` file to keep your API keys secure!

#### Option 2: Set Environment Variables Directly

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:FINANCE_AGENT_MODEL="gpt-4o"  # Optional, defaults to gpt-4o-mini
$env:ALPHA_VANTAGE_API_KEY="your-alpha-vantage-api-key-here"
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-openai-api-key-here
set FINANCE_AGENT_MODEL=gpt-4o
set ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key-here
```

**On Linux/Mac:**
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export FINANCE_AGENT_MODEL="gpt-4o"  # Optional, defaults to gpt-4o-mini
export ALPHA_VANTAGE_API_KEY="your-alpha-vantage-api-key-here"
```

**Environment Variables:**
- `OPENAI_API_KEY` (Required): Your OpenAI API key for the agent
- `FINANCE_AGENT_MODEL` (Optional): The OpenAI model to use (defaults to `gpt-4o-mini` if not set)
- `ALPHA_VANTAGE_API_KEY` (Optional): Your Alpha Vantage API key for stock data via MCP

### 3. Alpha Vantage MCP Server

The application uses Alpha Vantage's remote MCP server at `https://mcp.alphavantage.co/mcp`. No additional installation is required - just set your `ALPHA_VANTAGE_API_KEY` environment variable.

### 4. Run the Application

```bash
python app.py
```

The Gradio interface will launch in your browser at `http://localhost:7860`

## How It Works

1. **Finance Buddy Agent** (`ai-agents/finance-buddy.py`):
   - Contains the agent's configuration, model settings, and instructions
   - Reads the model from `FINANCE_AGENT_MODEL` environment variable (defaults to `gpt-4o-mini`)
   - Sets up MCP integration with Alpha Vantage remote server at `https://mcp.alphavantage.co/mcp`
   - Uses OpenAI Agents SDK to create the agent

2. **Gradio Interface** (`app.py`):
   - Provides a simple chat interface to interact with Finance Buddy
   - Handles conversation history
   - Uses trace logging to monitor agent execution
   - Falls back to direct OpenAI API calls if Agents SDK is not available

## Features

- Simple and understandable code structure
- MCP integration for Alpha Vantage financial data tools
- Friendly chat interface using Gradio
- Fallback support if Agents SDK is not available

## Notes

- The agent will use MCP tools from Alpha Vantage when `ALPHA_VANTAGE_API_KEY` is set
- The model can be configured via `FINANCE_AGENT_MODEL` environment variable (defaults to `gpt-4o-mini`)
- Agent execution is traced and logged for debugging purposes
- If the OpenAI Agents SDK is not installed, the app will fall back to direct OpenAI API calls
- Always consult with a licensed financial advisor for major investment decisions

## Troubleshooting

- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **API key errors**: Verify your environment variables are set correctly
- **MCP server errors**: Verify your `ALPHA_VANTAGE_API_KEY` is set correctly for the remote MCP server

