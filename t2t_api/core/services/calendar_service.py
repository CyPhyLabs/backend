# services/calendar_service.py

from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings
from ..models import PersonalCalendar  # Adjust the import path as needed

def create_google_calendar(summary, description=""):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_PATH

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)

    calendar = {
        'summary': summary,
        'description': description,
        'timeZone': 'America/Chicago',
    }

    created_calendar = service.calendars().insert(body=calendar).execute()

    return {
        'calendar_id': created_calendar['id'],
        'name': created_calendar['summary'],
        'description': created_calendar.get('description', '')
    }

def create_personal_calendar_for_user(user):
    calendar_data = create_google_calendar(f"{user.username}'s Calendar")
    return PersonalCalendar.objects.create(
        user=user,
        calendar_id=calendar_data["calendar_id"],
        calendar_name=calendar_data["name"],
        is_primary=True,
    )