import datetime
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# get_tasks() returns a list of tuples of the form (start_time, end_time, task)
# start_time and end_time are strings of the form "HH:MM" and task is a string
# notes_dir is the path to the directory where your daily notes are stored
def get_tasks(notes_dir):
    todays_date = datetime.date.today().strftime("%m-%d-%Y")
    todays_file = f"{notes_dir}/{todays_date}.md"
    tasks = []
    with open(todays_file, "r") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if line.startswith("# Day Planner"): # replace with your header if you use a different one
                local_idx = idx + 1
                next_line = lines[local_idx]
                while next_line != "\n":
                    parsed_line = next_line.split(" ") 
                    start_time = parsed_line[2] if "[x]" in parsed_line else parsed_line[3]
                    end_time = parsed_line[4] if "[x]" in parsed_line else parsed_line[5]
                    task = ' '.join(parsed_line[5:]) if "[x]" in parsed_line else ' '.join(parsed_line[6:])
                    task = task.replace("\n", "")
                    tasks.append((start_time, end_time, task))
                    local_idx += 1
                    next_line = lines[local_idx]
    return tasks

# Function to authenticate and create a service
def google_calendar_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service

# Function to add an event
def add_event(service, summary, start_time, end_time):
    event = {
      'summary': summary,
      'start': {
        'dateTime': start_time,
        'timeZone': 'America/New_York',
      },
      'end': {
        'dateTime': end_time,
        'timeZone': 'America/New_York',
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

if __name__ == "__main__":
    DAILY_NOTES_DIR = "<REPLACE WITH YOUR DIRECTORY>"
    tasks = get_tasks(DAILY_NOTES_DIR)
    service = google_calendar_service()
    date = datetime.date.today().strftime("%Y-%m-%d")
    for task in tasks:
        start, end, title = task
        start = f"{date}T{start}:00"
        end = f"{date}T{end}:00"
        print(start, end, title)
        add_event(service, title, start, end)











