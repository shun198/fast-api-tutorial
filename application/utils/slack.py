import logging
import requests
import os
import json


logger = logging.getLogger("uvicorn")


def send_slack_notification(message: str):
    try:
        alarm_emoji = ":rotating_light:"
        text = alarm_emoji + message
        data = json.dumps(
            {
                "attachments": [{"color": "#e01d5a", "text": text}],
            }
        )
        headers = {"Content-Type": "application/json"}
        requests.post(
            url=os.environ.get("SLACK_WEBHOOK_URL"), data=data, headers=headers
        )
    except Exception as e:
        logger.error(f"Slack送信エラー: {e}")
