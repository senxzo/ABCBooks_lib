import boto3
import json
import logging
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


"""Lambda function to send sns notifications to slack channel"""

# Environment Variables
HOOK_URL = os.environ['kmsEncryptedHookUrl']
SLACK_CHANNEL = os.environ['slackChannel']

# Setup Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log event data
    logger.info("Event: %s", str(event))

    # Extract SNS message directly
    sns_message = event['Records'][0]['Sns']['Message']
    
    # Access the required fields directly since sns_message is already a dictionary
    alarm_name = sns_message['AlarmName']
    new_state = sns_message['NewStateValue']
    reason = sns_message['NewStateReason']

    # Construct the Slack message
    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': f"{alarm_name} state is now {new_state}: {reason}"
    }

    # Prepare the request
    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))

    # Attempt to send the message to Slack
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
