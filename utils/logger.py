import logging
from pathlib import Path
from datetime import datetime

class Logger:
    """Centralized logging manager for the application."""
    @staticmethod
    def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
        """Sets up a logger with a file and console handler.

        Args:
            name: The name of the logger.
            level: The logging level.

        Returns:
            The configured logger instance.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if logger.handlers:
            return logger
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        log_file = logs_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger
