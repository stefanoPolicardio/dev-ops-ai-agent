import boto3
import datetime
import os

LOG_GROUP = "/aws/lambda/workshopLogGenerator:*"
LOGS_CLIENT = boto3.client("logs")

def lambda_handler(event, context):
    now = datetime.datetime.utcnow()
    start_time = int((now - datetime.timedelta(minutes=10)).timestamp() * 1000)
    end_time = int(now.timestamp() * 1000)

    response = LOGS_CLIENT.filter_log_events(
        logGroupName=LOG_GROUP,
        startTime=start_time,
        endTime=end_time,
    )

    messages = []
    for event in response.get("events", []):
        messages.append(event["message"])

    print(f"Recuperati {len(messages)} log:")
    for msg in messages:
        print(msg)

    return {
        "statusCode": 200,
        "count": len(messages),
        "messages": messages
    }
