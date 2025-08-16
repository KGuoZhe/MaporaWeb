# config.py
# ======================
# Central config for API keys and toggles
# ======================

import os
from dotenv import load_dotenv

load_dotenv()  # load .env if exists

# Toggle flags (easy switch)
USE_GOOGLE_API = False   # True to call Google Places API; False to use CSV
USE_LLM = False          # True to call real LLM; False to use fallback rules

# Keys (read from env or leave blank)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDUYluG7r9OEJncl4hnVyfIJWZUYcdh_fc")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default model name (only used when USE_LLM=True)
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")