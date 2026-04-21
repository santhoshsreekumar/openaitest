# openaitest

A Python project to interact with OpenAI's API via CLI or web interface.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set your OpenAI API key as an environment variable:**

**Windows (PowerShell):**
```powershell
$env:OPENAIKEY = "your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAIKEY=your-api-key-here
```

**macOS/Linux:**
```bash
export OPENAIKEY="your-api-key-here"
```

## Running the Project

### Option 1: CLI Tool (main.py)
Run the command-line interface with a prompt:

```bash
python main.py "Your prompt here"
```

**Example:**
```bash
python main.py "Explain quantum computing"
```

### Option 2: Web App (app.py)
Run the interactive Streamlit web application:

```bash
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY = ""
python -m streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## Features

- **CLI Mode:** Quick prompts from the terminal
- **Web Mode:** Interactive chat interface with a user-friendly UI
- **Secure:** Uses environment variables for API keys (never hardcoded)
- **Configurable:** Uses gpt-3.5-turbo model with adjustable parameters
