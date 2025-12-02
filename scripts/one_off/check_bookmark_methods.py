from atproto import Client
import os

handle = os.environ.get('BLUESKY_HANDLE_DEBUG', "jonathonmarsden.com")
password = os.environ.get('BLUESKY_PASSWORD_DEBUG', "gars-eqs3-ruay-ym35")
client = Client()
client.login(handle, password)

print(dir(client.app.bsky.bookmark))
