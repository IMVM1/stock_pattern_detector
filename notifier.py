import requests

def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a Telegram notification.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"Telegram sending failed: {str(e)}")
