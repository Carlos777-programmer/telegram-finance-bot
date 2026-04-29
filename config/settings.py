import os
from dotenv import load_dotenv

load_dotenv() 

TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = int(os.getenv("MY_TELEGRAM_ID"))