# GitHub Repository Analyzer

AI-powered tool for analyzing GitHub repositories, extracting build instructions from README files, and automating build execution. Supports multiple LLM backends including DSPy, OpenAI, and Ollama.

## Features

- Extracts build instructions from repository README files
- Executes automated dependency installation and build steps
- Compares repositories to identify missing files
- Continuous keyword-based scanning and auditing of public repositories
- Local LLM support via Ollama for offline analysis

## Prerequisites

- Python 3.10+
- GitHub API token
- OpenAI API key (optional, used as fallback)
- Ollama (optional, for local LLM inference)

## Installation

```bash
git clone https://github.com/Jimmyu2foru18/github-analyzer.git
cd github-analyzer
pip install -r requirements.txt
```

## Configuration

Copy `config.yaml` and fill in the required values:

```yaml
GITHUB_TOKEN: "your_github_token"
OPENAI_API_KEY: "your_openai_api_key"
MODEL_NAME: "gpt-4.0-mini"
BASE_DIRECTORY: "github-repos"
LOG_DIRECTORY: "logs"
OLLAMA_BASE_URL: "http://localhost:11434/api"
OLLAMA_MODEL: "llama3"
```

Environment variables override config file values:
- `GITHUB_TOKEN`
- `OPENAI_API_KEY`
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`

## Usage

### Analyze and Build a Repository

```bash
python main.py
```

Enter a GitHub repository URL when prompted. Optionally enter a second repository URL to compare file structures.

### Continuous Scanner

```bash
python scanner_main.py
```

Enter a keyword to search for and audit relevant repositories.

## Architecture

| Module | Responsibility |
|--------|---------------|
| `github_service.py` | GitHub API interactions: download, search, README extraction |
| `auto_builder.py` | Build automation and AI-driven analysis orchestration |
| `dspy_analyzer.py` | DSPy-based README analysis |
| `ollama_service.py` | Local LLM inference via Ollama |
| `scanner_service.py` | Automated scanning and auditing workflow |
| `config.py` | Configuration loading and validation |
| `logger.py` | Logging configuration |

## Analysis Pipeline

1. Read repository README
2. Attempt DSPy analysis
3. Fallback to Ollama if DSPy fails
4. Fallback to OpenAI if Ollama fails
5. Parse structured build instructions
6. Execute dependency installation and build steps

## License

MIT