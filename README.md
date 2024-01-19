# Demo


https://github.com/spcoughlin/obsidian-google-calendar/assets/99555305/618ce4c2-5a6c-45c3-988f-cd2da57a6f0a


# Setup
## Guide: Formatting Day Planner

Day Planner stores daily schedule in raw markdown, like:

```
# Day Planner
- [ ] 9:10 - 12:20 Do stuff
- [ ] 13:00 - 14:00 Do more stuff
```

This is how you should format the Day Planner section of your daily note to be compatible with the script. The script is designed to parse each task in this format exactly, so make sure spaces are correct. You can still check off your tasks, and it will not affect the script. Also see demo.

## Prerequisites

Obsidian with Day Planner Plugin, Daily Notes set up with a template that has a Day Planner Heading.

## Google API

To add an event to your Google Calendar, you will need to configure the Google Calendar API. Here's a step-by-step guide on how to accomplish this:

https://developers.google.com/calendar/api/quickstart/python

Follow the quickstart up to "Install the Google Client Library"

# Installation

Clone the repository, replace the credentials.json file with the one you got from Google, and delete `token.json`. Replace the directory variable in the `if __name__ == __main__:`  section at the bottom of the script, with the directory where your daily notes are created and stored. 

A new `token.json` will be created when the program is run for the first time, and the application is authenticated.

# Recommended aliases

I made aliases for the scripts, "gcal-fill" which calls the main script, "gcal-delete" which calls the delete script, and "gcal-update" which calls gcal-delete && gcal-fill
