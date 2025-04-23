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

def fetch_events(calendar_id, time_min=None, time_max=None, query=None):
    """
    Fetch events from Google Calendar with optional time range and search query.
    
    Args:
        calendar_id (str): The Google Calendar ID
        time_min (datetime or str): Start time for fetching events
        time_max (datetime or str): End time for fetching events
        query (str): Optional search term
    
    Returns:
        list: List of formatted calendar events
    """
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
        events = events_result.get('items', [])
        logger.debug(f"Retrieved {len(events)} events from Google Calendar")
        
        # Format the events for consistent output
        formatted_events = []
        for event in events:
            try:
                formatted_event = {
                    'id': event.get('id'),
                    'title': event.get('summary'),
                    'description': event.get('description'),
                    'location': event.get('location'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'end': event['end'].get('dateTime', event['end'].get('date')),
                    'created': event.get('created'),
                    'updated': event.get('updated'),
                    'status': event.get('status'),
                    'organizer': event.get('organizer', {}).get('email'),
                }
                formatted_events.append(formatted_event)
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
