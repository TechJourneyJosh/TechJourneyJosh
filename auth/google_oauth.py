"""
Run this once to generate your GOOGLE_REFRESH_TOKEN.
Usage: python auth/google_oauth.py
"""

import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]

CLIENT_CONFIG = {
    "installed": {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
    }
}


def main():
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n--- Copy this into your .env file ---")
    print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
    print("-------------------------------------\n")

    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }
    with open("auth/token.json", "w") as f:
        json.dump(token_data, f, indent=2)
    print("Token also saved to auth/token.json")


if __name__ == "__main__":
    main()
