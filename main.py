from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CLIENT_API")

# connect to the youtube function by using this build service from google api client
youtube = build("youtube", "v3", developerKey=api_key)

request = youtube.channels().list(
    part='statistics',
    forUsername='schafer5'
)

response = request.execute()
print(response)