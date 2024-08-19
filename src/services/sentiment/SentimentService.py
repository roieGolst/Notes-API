import os
import requests

LANGUAGE = "en"
URL = "https://api.meaningcloud.com/sentiment-2.1"
API_KEY = os.getenv("SENTIMENT_API_KEY")


def analyze_sentiment(content: str):
    payload = {
        'key': os.getenv("SENTIMENT_API_KEY"),
        'txt': content,
        'lang': LANGUAGE
    }

    response = requests.post(URL, data=payload)

    return response.json()