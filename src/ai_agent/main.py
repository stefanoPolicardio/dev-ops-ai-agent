from ai_agent.agent import run_agent
from ai_agent.utils import logger
import time

def lambda_handler(event, context):
    """AWS Lambda handler.
    
    Args:
        event: Lambda event data.
        context: Lambda runtime context.
        
    Returns:
        dict: Lambda response with statusCode and body.
    """
    logger.info("Lambda handler started")
    
    try:
        # Extract log message from event
        log_message = event.get("log_message", "Server error")
        logger.info(f"Processing event with log message: {log_message[:100]}...")
        
        # Run the AI agent
        result = run_agent(log_message)
        
        # Return response
        response = {"statusCode": 200, "body": result}
        logger.info("Lambda handler completed successfully")
        return response
        
    except Exception as e:
        # Return error response
        logger.error(f"Lambda handler failed: {str(e)}")
        return {
            "statusCode": 500, 
            "body": f"Lambda error: {str(e)}"
        }

"""
    "log_message": "2025-05-26T10:45:02.147Z [WARN] [order-service] [OrderProcessor.java:124] Service responded in 18.3s – usually takes <5s. Feels like something's off."
    "log_message": "2025-05-26T10:45:05.392Z [INFO] [checkout-lambda] [CheckoutHandler.py:87] No exception thrown, but customer complaints about "endless loading."
    "log_message": "2025-05-26T10:45:09.908Z [ERROR] [payment-service] [DnsResolver.kt:42] Possible DNS resolution delays? Observed delays across several services."
"""

def cli_runner():
    """CLI wrapper to run lambda_handler for Poetry script."""
    logger.info("CLI runner started")
    
    # Mock event and context for CLI execution
    mock_event = {
       #"log_message": "2025-05-26T10:45:05.392Z [INFO] [checkout-lambda] [CheckoutHandler.py:87] No exception thrown, but customer complaints about 'endless loading.'",
       #"log_message": "2025-05-26T10:45:02.147Z [WARN] [order-service] [OrderProcessor.java:124] Service responded in 18.3s – usually takes <5s. Feels like something's off.",
       #"log_message": "2025-05-26T10:45:09.908Z [ERROR] [payment-service] [DnsResolver.kt:42] Possible DNS resolution delays? Observed delays across several services.",
       #"log_message": "2025-05-26T10:45:11.215Z [ERROR] [notification-service] [EmailSender.java:342] java.lang.OutOfMemoryError: Java heap space – service not responding after repeated GC cycles.",
       "log_message": "INIT_START Runtime Version: python:3.13.v43\\tRuntime Version ARN: arn:aws:lambda:us-east-1::runtime:dacbb0d790375a116fa3966c89301588288d4a1ebd0c61a55d46fba286c00e84",
        "user_id": "cli_user",
        "source": "cli"
    }
    
    class MockContext:
        aws_request_id = "cli-request-123"
        function_name = "ai-agent-cli"
        function_version = "$LATEST"
        memory_limit_in_mb = 512
        
        def get_remaining_time_in_millis(self):
            return 30000  # 30 seconds for CLI testing
    
    mock_context = MockContext()
    
    print("Running Lambda handler...")
    
    try:
        result = lambda_handler(mock_event, mock_context)
        print(f"Result: {result}")
        logger.info("CLI runner completed successfully")
        return result
        
    except Exception as e:
        error_msg = f"CLI execution failed: {str(e)}"
        print(error_msg)
        logger.error(f"CLI runner failed: {str(e)}")
        return {"statusCode": 500, "body": error_msg}


if __name__ == "__main__":
    cli_runner()
