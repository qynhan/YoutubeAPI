from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import re
from datetime import timedelta

load_dotenv()

api_key = os.getenv("CLIENT_API")

# connect to the youtube function by using this build service from google api client
youtube = build("youtube", "v3", developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')


nextPageToken = None
total_seconds = 0

while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId="PLXcWclJxzYCQCk_o7Rwt6Ma8wA7UAw3AF",
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []
    for item in pl_response['items']:
        vid_id = item['contentDetails']['videoId']
        vid_ids.append(vid_id)


    vid_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    


    for item in vid_response["items"]:
        duration = item["contentDetails"]["duration"]

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()

        total_seconds += video_seconds

    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

total_seconds = int(total_seconds)
minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)
print(f'{hours}:{minutes}:{seconds}')