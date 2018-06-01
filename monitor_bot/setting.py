import os
API_KEY = os.environ.get('BOT_KEY', False)
if not API_KEY:
    raise Exception("Please set slack API key as a environment variable, BOT_KEY.")
