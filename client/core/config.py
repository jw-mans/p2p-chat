import os
from dotenv import load_dotenv

load_dotenv()
DISCOVERY_URL = os.getenv("DISCOVERY_URL")
ACCOUNT_FILE=os.getenv("ACCOUNT_FILE")