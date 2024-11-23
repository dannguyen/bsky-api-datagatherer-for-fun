from atproto import Client
from pathlib import Path

USERNAME = "dancow.bsky.social"
PASSKEY = Path(".key").read_text().strip()

client = Client()
client.login(USERNAME, PASSKEY)
# post = client.send_post("""Hello world!
# I just followed the bluesky guide at https://docs.bsky.app/docs/get-started#create-a-post
# to make a skeet with python.
# """)


# response = client.app.bsky.graph.get_lists({'actor': USERNAME})
# user_lists = response['lists']
# mydid = client.me.did

response = client.com.atproto.graph.get_list_memberships(actor=USERNAME)


resp = client.app.bsky.feed.search_posts(params={"q": "dancow", "cursor": None})
posts = list(resp.posts)
for p in resp.posts:
    print(f"{p.author.handle}:\n {p.record.text}")
