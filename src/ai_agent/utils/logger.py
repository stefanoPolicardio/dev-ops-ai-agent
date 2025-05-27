"""Simple logging configuration for the AI Agent."""

import logging
from datetime import datetime
from typing import Optional



class LoggerConfig:
    """Simple singleton logger configuration."""
    
    _logger: Optional[logging.Logger] = None
    
    @classmethod
    def get_logger(cls, name: str = "ai_agent") -> logging.Logger:
        """Get the singleton logger instance.
        
        Args:
            name (str): Logger name (unused after first call).
            
        Returns:
            logging.Logger: Configured logger instance.
        """
        if cls._logger is None:
            cls._logger = cls._create_logger(name)
        
        return cls._logger
    
    @classmethod
    def _create_logger(cls, name: str) -> logging.Logger:
        """Create and configure the logger.
        
        Args:
            name (str): Logger name.
            
        Returns:
            logging.Logger: Configured logger instance.
        """
        log_format = (
        "%(asctime)s.%(msecs)03d [%(levelname)s]  [%(filename)s:%(lineno)d] %(message)s"
        )


        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if logger.hasHandlers():
            logger.handlers.clear()

        handler = logging.StreamHandler()
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False    
        
        return logger


# Global logger instance for easy import
logger = LoggerConfig.get_logger() 