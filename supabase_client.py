"""
supabase_client.py
-------------------
Initialises and exposes a singleton Supabase client.
Reads credentials from .env (copy .env.example → .env and fill in your values).
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_client: Client | None = None


def get_supabase() -> Client:
    global _client
    if _client is None:
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise EnvironmentError(
                "SUPABASE_URL and SUPABASE_KEY must be set in your .env file. "
                "Copy .env.example to .env and fill in your Supabase credentials."
            )
        _client = create_client(url, key)
    return _client