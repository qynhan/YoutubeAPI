from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CLIENT_API")

# connect to the youtube function by using this build service from google api client
youtube = build("youtube", "v3", developerKey=api_key)

nextPageToken = None
videos = []
playlist_id = "PLXcWclJxzYCQCk_o7Rwt6Ma8wA7UAw3AF"

while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []
    for item in pl_response['items']:
        vid_id = item['contentDetails']['videoId']
        vid_ids.append(vid_id)

    
    vid_request = youtube.videos().list(
        part="statistics",
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    for item in vid_response["items"]:
        vid_views = item["statistics"]["viewCount"]
        vid_id = item['id']
        yt_link = f'https://youtu.be/{vid_id}'

        videos.append(
            {
                "views": int(vid_views),
                "url": yt_link
            }
        )

    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

videos.sort(key=lambda vid: vid["views"], reverse=True)

for video in videos[:10]:
    print(video["url"], video["views"])
