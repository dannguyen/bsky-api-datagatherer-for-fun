from atproto import Client
import rich_click as click


def get_client(username: str, passkey: str):
    client = Client()
    client.login(username, passkey)
    return client


def get_profiles(client, actors: list[str]) -> list[dict]:
    """
    https://docs.bsky.app/docs/tutorials/viewing-profiles
    """
    resp = client.get_profiles(actors)
    profilelist = resp.dict()["profiles"]
    return profilelist


def get_followers(client, username: str) -> None:
    _iter = 0
    cursor = None
    # by default, we'll collect followers

    try:
        while _iter == 0 or cursor is not None:
            fetched = client.app.bsky.graph.get_followers(
                params={"actor": username, "cursor": cursor}
            )

            _iter += 1
            batchdata = fetched.followers
            yield _iter, batchdata

            cursor = fetched.cursor
    except Exception as e:
        raise e
