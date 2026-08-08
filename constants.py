from enum import Enum
from pathlib import Path

class BuildStepType(Enum):
    SETUP = "setup"
    BUILD = "build"
    TEST = "test"

# File system constants
DEFAULT_BASE_DIR = Path("github-repos")
DEFAULT_LOG_DIR = Path("logs")

# API constants
DEFAULT_MODEL = "gpt-4.0-mini"
DEFAULT_OLLAMA_URL = "http://localhost:11434/api"
DEFAULT_OLLAMA_MODEL = "llama3"

# Timeouts and retries
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3 