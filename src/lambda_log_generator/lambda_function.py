import logging
import datetime
import random
import os

# Lista di messaggi con metadati
LOG_ENTRIES = [
    {
        "level": "INFO",
        "service": "checkout-lambda",
        "location": "CheckoutHandler.py:87",
        "message": "No exception thrown, but customer complaints about 'endless loading.'"
    },
    {
        "level": "WARN",
        "service": "order-service",
        "location": "OrderProcessor.java:124",
        "message": "Service responded in 18.3s – usually takes <5s. Feels like something's off."
    },
    {
        "level": "ERROR",
        "service": "payment-service",
        "location": "DnsResolver.kt:42",
        "message": "Possible DNS resolution delays? Observed delays across several services."
    },
    {
        "level": "ERROR",
        "service": "notification-service",
        "location": "EmailSender.java:342",
        "message": "java.lang.OutOfMemoryError: Java heap space – service not responding after repeated GC cycles."
    }
]

def lambda_handler(event, context):
    now = datetime.datetime.utcnow().isoformat(timespec='milliseconds') + "Z"
    
    # Seleziona un log casuale
    entry = random.choice(LOG_ENTRIES)

    # Costruisce messaggio completo nel formato standardizzato
    formatted_log = f"{entry['message']}"

    logger = get_configured_logger()

    # Switch-case sul livello
    match entry['level']:
        case "INFO":
            logger.info(formatted_log)
        case "WARN":
            logger.warning(formatted_log)
        case "ERROR":
            logger.error(formatted_log)
        case _:
            logger.debug(formatted_log)  # fallback in caso di livello sconosciuto

    return {
        "statusCode": 200,
        "body": {
            "log": formatted_log
        }
    }

def get_configured_logger(name: str = None) -> logging.Logger:
    """
    Ritorna un logger configurato con formato:
    {timestamp} [LEVEL] [lambda] [file:line] message

    :param name: nome del logger (default root)
    :return: logger configurato
    """

    lambda_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME", "local-lambda")

    log_format = (
        "%(asctime)s.%(msecs)03d [%(levelname)s] [" + lambda_name + "] [%(filename)s:%(lineno)d] %(message)s"
    )


    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

