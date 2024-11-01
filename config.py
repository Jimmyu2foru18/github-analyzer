from dataclasses import dataclass
from typing import Optional
import os
import yaml
from pathlib import Path
from constants import (
    DEFAULT_BASE_DIR, DEFAULT_LOG_DIR, DEFAULT_MODEL,
    DEFAULT_TIMEOUT, DEFAULT_MAX_RETRIES
)

@dataclass
class Config:
    GITHUB_TOKEN: str
    OPENAI_API_KEY: str
    BASE_DIRECTORY: Path
    LOG_DIRECTORY: Path
    MODEL_NAME: str = DEFAULT_MODEL
    MAX_RETRIES: int = DEFAULT_MAX_RETRIES
    TIMEOUT: int = DEFAULT_TIMEOUT
    
    @classmethod
    def from_yaml(cls, config_path: str = "config.yaml") -> 'Config':
        """
        Load configuration from YAML file with environment variable override.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            Config: Configuration object
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is invalid
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
        try:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML configuration: {e}")
        
        # Environment variables override file config
        config_data['GITHUB_TOKEN'] = os.getenv('GITHUB_TOKEN', config_data.get('GITHUB_TOKEN'))
        config_data['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', config_data.get('OPENAI_API_KEY'))
        
        # Convert string paths to Path objects
        config_data['BASE_DIRECTORY'] = Path(config_data.get('BASE_DIRECTORY', DEFAULT_BASE_DIR))
        config_data['LOG_DIRECTORY'] = Path(config_data.get('LOG_DIRECTORY', DEFAULT_LOG_DIR))
        
        return cls(**config_data)
    
    def validate(self) -> None:
        """
        Validate configuration and create necessary directories.
        
        Raises:
            ValueError: If required configuration is missing
            PermissionError: If directory creation fails
        """
        if not self.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is required")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
            
        try:
            # Create directories
            self.BASE_DIRECTORY.mkdir(parents=True, exist_ok=True)
            self.LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise PermissionError(f"Failed to create directory: {e}")