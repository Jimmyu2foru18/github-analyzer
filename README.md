# GitHub Repository Analyzer

An intelligent tool that leverages AI to analyze GitHub repositories, automate build processes, and compare codebases. Built with Python, OpenAI GPT, and DSPy.

## 🚀 Features

- **Repository Analysis**: Automatically download and analyze GitHub repositories
- **AI-Powered Build Instructions**: Extract build steps from README files using OpenAI GPT and DSPy
- **Automated Building**: Execute extracted build instructions automatically
- **Repository Comparison**: Compare two repositories to find missing files
- **Comprehensive Logging**: Detailed logging system for debugging and monitoring

## 🔧 Prerequisites

- Python 3.8 or higher
- GitHub API Token ([How to get one](https://github.com/settings/tokens))
- OpenAI API Key ([Get from OpenAI](https://platform.openai.com/api-keys))

## 📦 Installation

1. Clone the repository:

bash
git clone https://github.com/Jimmyu2foru18/github-analyzer.git
cd github-analyzer


2. Run the development setup script:

bash
run_project_dev.bat


The script will:
- Create a virtual environment
- Install required dependencies
- Prompt for API keys if not set
- Start the analyzer

## ⚙️ Configuration

1. Environment Variables:
   - `GITHUB_TOKEN`: Your GitHub API token
   - `OPENAI_API_KEY`: Your OpenAI API key

2. Configuration File (`config.yaml`):

yaml
MODEL_NAME: "gpt-4.0-mini"
BASE_DIRECTORY: "github-repos"
LOG_DIRECTORY: "logs"
DSPY_SETTINGS:
cache_dir: "cache/dspy"
temperature: 0.1
max_tokens: 1000

## 🚀 Usage

1. Start the analyzer:

bash
python main.py


2. When prompted:
   - Enter the URL of the repository you want to analyze
   - Optionally enter a second repository URL for comparison

3. The tool will:
   - Download the repository
   - Extract build instructions from README
   - Execute build steps automatically
   - Compare repositories if a second URL was provided
   - Generate detailed logs in the `logs` directory

## 📁 Project Structure

github-analyzer/
├── auto_builder.py # Build automation logic
├── config.py # Configuration management
├── constants.py # Project constants
├── decorators.py # Utility decorators
├── dspy_analyzer.py # DSPy analysis implementation
├── exceptions.py # Custom exceptions
├── github_service.py # GitHub API interactions
├── logger.py # Logging setup
├── main.py # Main entry point
└── requirements.txt # Project dependencies


## 🔍 Error Handling

The project includes comprehensive error handling:
- GitHub API errors
- Build process failures
- Configuration issues
- Network connectivity problems

Check the `logs` directory for detailed error information.

## 🙏 Acknowledgments

- OpenAI for GPT API
- DSPy for the analysis framework
- GitHub API for repository access