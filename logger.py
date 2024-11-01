import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logger(name: str, log_level: str = "INFO", log_dir: Optional[Path] = None) -> logging.Logger:
    """Set up a logger with console and optional file handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Optional directory for log files
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
        
    # Create formatters
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] {%(name)s} %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_dir:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create daily log file
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = log_dir / f"{name}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    return logger