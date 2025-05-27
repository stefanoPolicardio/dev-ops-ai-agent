"""Example of how to use the logger in different classes and functions."""

from ai_agent.utils import logger


class ExampleService:
    """Example service class showing logger usage."""
    
    def __init__(self):
        logger.info("ExampleService initialized")
    
    def process_data(self, data: str) -> str:
        """Process some data with logging."""
        logger.info(f"Processing data: {data[:50]}...")
        
        try:
            # Simulate some processing
            result = f"Processed: {data.upper()}"
            logger.info("Data processing completed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Data processing failed: {str(e)}")
            raise


def standalone_function(message: str) -> None:
    """Standalone function showing logger usage."""
    logger.info(f"Standalone function called with: {message}")
    
    if not message:
        logger.warning("Empty message received")
        return
    
    logger.info("Processing message...")
    # Simulate processing
    logger.info("Message processed successfully")


if __name__ == "__main__":
    # Example usage
    logger.info("Starting logger usage example")
    
    # Class usage
    service = ExampleService()
    result = service.process_data("Hello World")
    logger.info(f"Service returned: {result}")
    
    # Function usage
    standalone_function("Test message")
    standalone_function("")  # This will trigger a warning
    
    logger.info("Logger usage example completed") 