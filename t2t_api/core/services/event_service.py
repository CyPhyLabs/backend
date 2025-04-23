from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings
from datetime import datetime

def get_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_PATH
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=credentials)

def format_google_event(event):
    return {
        "id": event.get("id"),
        "title": event.get("summary"),
        "description": event.get("description"),
        "location": event.get("location"),
        "start": event["start"].get("dateTime", event["start"].get("date")),
        "end": event["end"].get("dateTime", event["end"].get("date")),
        'audience': event.get('extendedProperties', {}).get('private', {}).get('audience', 'everyone'),
        "status": event.get("status"),
        "htmlLink": event.get("htmlLink"),  # optional: frontend might use this

    }


def fetch_events(calendar_id, time_min=None, time_max=None, query=None, audience=None):
    service = get_calendar_service()
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Base parameters for the API call
        params = {
            'singleEvents': True,
            'orderBy': 'startTime',
            'maxResults': 2500
        }
        
        # Handle time_min parameter
        if time_min:
            if isinstance(time_min, str):
                try:
                    # Remove 'Z' if present and parse the datetime
                    time_min = datetime.fromisoformat(time_min.replace('Z', ''))
                except ValueError as e:
                    logger.error(f"Invalid time_min format: {time_min}")
                    raise ValueError(f"Invalid time_min format: {e}")
            params['timeMin'] = time_min.isoformat() + 'Z'
            logger.debug(f"Using timeMin: {params['timeMin']}")
        
        # Handle time_max parameter
        if time_max:
            if isinstance(time_max, str):
                try:
                    # Remove 'Z' if present and parse the datetime
                    time_max = datetime.fromisoformat(time_max.replace('Z', ''))
                except ValueError as e:
                    logger.error(f"Invalid time_max format: {time_max}")
                    raise ValueError(f"Invalid time_max format: {e}")
            params['timeMax'] = time_max.isoformat() + 'Z'
            logger.debug(f"Using timeMax: {params['timeMax']}")
        
        # Add search query if provided
        if query:
            params['q'] = query
            logger.debug(f"Using search query: {query}")
        
        # Make the API call
        logger.debug(f"Calling Google Calendar API with params: {params}")
        events_result = service.events().list(calendarId=calendar_id, **params).execute()
        raw_events = events_result.get('items', [])
        logger.debug(f"Retrieved {len(raw_events)} events from Google Calendar")

        raw_events = events_result.get('items', [])

        # Filter events based on audience
        filtered_events = []
        for event in raw_events:
            event_audience = (
                event.get('extendedProperties', {})
                    .get('private', {})
                    .get('audience', 'everyone')
            )
            # if audience is None or audience == event_audience or event_audience == 'everyone':
            if event_audience == 'everyone' or event_audience == audience or audience is None:
                filtered_events.append(event)
        
        # Format the events for consistent output
        formatted_events = []
        for event in filtered_events:
            try:
                formatted_events.append(format_google_event(event))
            except KeyError as e:
                logger.warning(f"Skipping malformed event: {e}")
                continue
        
        logger.debug(f"Successfully formatted {len(formatted_events)} events")
        return formatted_events
        
    except Exception as e:
        logger.error(f"Error fetching events: {str(e)}", exc_info=True)
        raise Exception(f"Failed to fetch events: {str(e)}")

def create_event(calendar_id, event_data):
    service = get_calendar_service()
    return service.events().insert(calendarId=calendar_id, body=event_data).execute()

def update_event(calendar_id, event_id, updated_data):
    service = get_calendar_service()
    return service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_data).execute()

def delete_event(calendar_id, event_id):
    service = get_calendar_service()
    return service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
