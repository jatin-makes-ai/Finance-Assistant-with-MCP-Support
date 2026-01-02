# Finance Buddy 💸

A smart financial advisor agent powered by **OpenAI Agents** and **Alpha Vantage MCP**.

## 🚀 Features

- **AI Financial Advisor**: An intelligent agent capable of answering financial queries.
- **Real-time Data**: Integrates with Alpha Vantage for live stock market data via MCP (Model Context Protocol).
- **Dual Interface**:
  - **Web UI**: User-friendly chat interface using Gradio.
  - **CLI**: Command-line tool for quick testing.

## 📂 Project Structure

```text
Financial-Advisor/
├── ai-agents/          # Agent logic and configuration
├── app.py              # Gradio Web Interface
├── main.py             # CLI Runner for testing
├── mcp_manager.py      # MCP Server connection manager
├── mcp.json            # MCP configurations
└── requirements.txt    # Dependencies
```

## 🛠️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_key
ALPHA_VANTAGE_API_KEY=your_alphavantage_key
FINANCE_AGENT_MODEL=gpt-4o-mini  # Optional
```

## 🏃 Usage

### Run Web Interface

Launch the Gradio chat app:

```bash
python app.py
```
Access at: `http://localhost:7860`

### Run CLI Test

Execute a test query in the terminal:

```bash
python main.py
```

## 🔧 Configuration

The project uses `mcp.json` to configure MCP servers. By default, it is set up for Alpha Vantage:

```json
{
  "servers": {
    "alphavantage": {
      "type": "http",
      "url": "https://mcp.alphavantage.co/mcp?apikey=YOUR_API_KEY"
    }
  }
}
```

## ⚠️ Troubleshooting

- **Connection Errors**: Ensure your API keys in `.env` are correct.
- **Dependencies**: Re-run `pip install -r requirements.txt` if modules are missing.

---
*Disclaimer: This is an AI tool. Always consult a licensed financial advisor for investment decisions.*
