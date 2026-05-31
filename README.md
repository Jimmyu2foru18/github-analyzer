# GitHub Repository Analyzer

This tool uses AI to analyze GitHub repositories, automate build processes, compare codebases, and perform continuous background scanning with optional local LLM support via Ollama.

## Key Features

* **AI-Powered Analysis:** Extracts build instructions from README files using DSPy, OpenAI, or local LLMs (via Ollama).
* **Automated Building:** Executes extracted build instructions automatically.
* **Continuous Scanning:** Automated background scanning and auditing of repositories based on keyword searches.
* **Repository Comparison:** Compares repositories to find missing files.
* **Local LLM Integration:** Full support for running analysis locally using [Ollama](https://ollama.com/).

## Prerequisites

* Python 3.10+
* GitHub API Token ([How to get one](https://github.com/settings/tokens))
* (Optional) OpenAI API Key
* (Optional) [Ollama](https://ollama.com/) installed and running locally

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jimmyu2foru18/github-analyzer.git
   cd github-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set your environment variables or update `config.yaml`:

* `GITHUB_TOKEN`: Your GitHub API token (Required)
* `OPENAI_API_KEY`: Your OpenAI API key (Optional, used as fallback)
* `OLLAMA_BASE_URL`: URL to your Ollama API (Default: `http://localhost:11434/api`)
* `OLLAMA_MODEL`: Model to use (Default: `llama3`)

## Usage

### 1. Analyze & Build
```bash
python main.py
```

### 2. Continuous Scanner
```bash
python scanner_main.py
```
(Enter a keyword to start scanning and auditing relevant repositories.)

## Architecture

* `github_service.py`: GitHub API interactions (download, search).
* `ollama_service.py`: Interface for local LLMs via Ollama.
* `scanner_service.py`: Orchestrates automated scanning and auditing.
* `auto_builder.py`: Build automation and AI-driven analysis.

## Acknowledgments

* OpenAI for the GPT API
* DSPy for the analysis framework
* Ollama for local LLM capability
* GitHub API for repository access
