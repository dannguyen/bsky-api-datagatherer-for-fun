from atproto import Client
from pathlib import Path

USERNAME = "dancow.bsky.social"
PASSKEY = Path(".key").read_text().strip()

client = Client()
client.login(USERNAME, PASSKEY)
post = client.send_post(
    """Hello world!
I just followed the bluesky guide at https://docs.bsky.app/docs/get-started#create-a-post
to make a skeet with python.
"""
)
