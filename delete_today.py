# delete all events from today
# works off of the same credentials.json that is already in the directory
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import datetime
import pytz
import os

# Function to authenticate and create a service
def google_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('/Users/seancoughlin/projects/obsidianGCal/token.json'):
        creds = Credentials.from_authorized_user_file('/Users/seancoughlin/projects/obsidianGCal/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/seancoughlin/projects/obsidianGCal/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('/Users/seancoughlin/projects/obsidianGCal/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to delete all events today
def delete_events_today(service, timezone_str="America/New_York"):
    # Get current date in the correct format
    timezone = pytz.timezone(timezone_str)
    today = datetime.datetime.now(timezone).date()
    tomorrow = today + datetime.timedelta(days=1)

    # Convert local time to UTC for the API
    time_min = timezone.localize(datetime.datetime.combine(today, datetime.time.min)).isoformat()
    time_max = timezone.localize(datetime.datetime.combine(tomorrow, datetime.time.min)).isoformat()

    events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                          singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No events found for today.')
    else:
        for event in events:
            service.events().delete(calendarId='primary', eventId=event['id']).execute()
            print(f"Event deleted: {event['summary']}")

# Example usage
if __name__ == '__main__':
    service = google_calendar_service()
    delete_events_today(service, "America/New_York")







