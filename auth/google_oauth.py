"""
Run this once to generate your GOOGLE_REFRESH_TOKEN.
Works on GitHub Codespaces, Replit, and local machines.

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

# Port 8080 works with Codespaces and Replit port forwarding
PORT = int(os.environ.get("OAUTH_PORT", 8080))


def main():
    flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)

    print(f"\nStarting OAuth server on port {PORT}...")
    print("If you are on Codespaces or Replit, look for a port-forwarding popup.\n")

    creds = flow.run_local_server(port=PORT, open_browser=True)

    print("\n--- Copy this into your .env file ---")
    print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
    print("-------------------------------------\n")

    os.makedirs("auth", exist_ok=True)
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes),
    }
    with open("auth/token.json", "w") as f:
        json.dump(token_data, f, indent=2)
    print("Token also saved to auth/token.json")


if __name__ == "__main__":
    main()
