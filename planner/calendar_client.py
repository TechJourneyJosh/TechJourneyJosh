import os
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def _get_credentials() -> Credentials:
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return creds


def get_service():
    return build("calendar", "v3", credentials=_get_credentials())


def list_events(max_results: int = 10, calendar_id: str = "primary") -> list[dict]:
    service = get_service()
    now = datetime.now(timezone.utc).isoformat()
    result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return result.get("items", [])


def create_event(
    summary: str,
    start: str,
    end: str,
    description: str = "",
    calendar_id: str = "primary",
) -> dict:
    service = get_service()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start, "timeZone": "UTC"},
        "end": {"dateTime": end, "timeZone": "UTC"},
    }
    return service.events().insert(calendarId=calendar_id, body=event).execute()


def delete_event(event_id: str, calendar_id: str = "primary") -> None:
    service = get_service()
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
