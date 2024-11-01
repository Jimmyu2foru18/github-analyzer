from enum import Enum
from pathlib import Path

class BuildStepType(Enum):
    SETUP = "setup"
    BUILD = "build"
    TEST = "test"

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

# File system constants
DEFAULT_BASE_DIR = Path("github-repos")
DEFAULT_LOG_DIR = Path("logs")
DEFAULT_CACHE_DIR = Path("cache")

# API constants
DEFAULT_MODEL = "gpt-4.0-mini"
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TEMPERATURE = 0.1

# Timeouts and retries
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_RETRIES = 3

# File patterns
README_PATTERNS = ["README.md", "README.rst", "README.txt"] 