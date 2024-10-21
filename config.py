#APIキーやBOTトークンを管理
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY') 
BOT_TOKEN=os.getenv('BOT_TOKEN') 
