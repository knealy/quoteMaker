import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
INSTAGRAM_USERNAME = os.environ.get("spicy.fades")
INSTAGRAM_PASSWORD = os.environ.get("Apples123!")

# News Sources
NEWS_SOURCES = [
    {"name": "CNBC", "url": "https://www.cnbc.com/finance/"},
    {"name": "Bloomberg", "url": "https://www.bloomberg.com/markets"},
    {"name": "Yahoo Finance", "url": "https://finance.yahoo.com/"},
    {"name": "MarketWatch", "url": "https://www.marketwatch.com/"},
    {"name": "Financial Times", "url": "https://www.ft.com/markets"}
]

# UI Configuration
BACKGROUND_COLORS = [
    "#1E88E5", "#43A047", "#E53935", "#5E35B1", "#FB8C00", 
    "#00ACC1", "#3949AB", "#8E24AA", "#D81B60", "#7CB342"
]

# Quote Formatting Settings
MAX_QUOTE_LENGTH = 200 