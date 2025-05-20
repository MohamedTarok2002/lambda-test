import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Extract the code from the event payload
    code = event.get('code', '')

    logger.info("Received code:")
    logger.info(code)

    # WARNING: Executing arbitrary code can be very dangerous!
    # Only enable this if you fully trust the code source and understand the risks.
    try:
        exec(code)
        logger.info("Code executed successfully.")
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Code received and executed"})
    }
