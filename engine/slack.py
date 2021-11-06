import os
from dotenv import load_dotenv
import requests
import json

load_dotenv() #環境変数のロード

class Slack():
    
    @ staticmethod
    def send_message_webhook(url:str, message:str):
        pass