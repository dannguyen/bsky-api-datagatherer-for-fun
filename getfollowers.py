#!/usr/bin/env python3
"""
https://docs.bsky.app/docs/api/app-bsky-graph-get-followers
TODO:
hydrate follower counts and other metrics
get common followers?
"""


from atproto import Client
from pathlib import Path
import rich_click as click
import json

PASSKEY_PATH = Path(".key")


def get_client(username: str, passkey: str):
    client = Client()
    client.login(username, passkey)
    return client



def get_profiles(client, actors:list[str]) -> list[dict]:
    """
    https://docs.bsky.app/docs/tutorials/viewing-profiles
    """
    resp = client.get_profiles(actors)
    profilelist = resp.dict()['profiles']
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
        click.secho(f"Error occurred: {e}", err=True, fg="red")
        return


@click.command()
@click.option(
    "--username",
    "-u",
    default="dancow.bsky.social",
    help=f"A bluesky user handle, domain and all, e.g. jay.bsky.app",
    required=False,
    show_default=True,
    type=click.STRING,
)
@click.option(
    "--output-path",
    "-o",
    default="-",
    help=f"Set the path of the output file. Default is printing to stdout.",
    required=False,
    show_default=False,
    type=click.Path(dir_okay=False, path_type=Path, resolve_path=True),
)
@click.option(
    "--keyfile",
    "-k",
    default=".key",
    help=f"The file path where the bluesky passkey exists",
    required=False,
    show_default=True,
    type=click.Path(dir_okay=False, path_type=Path, resolve_path=True, exists=True),
)
def cli(username, keyfile, output_path):
    click.secho(
        f"Fetching data for {username}",
        err=True,
        bg="white",
        fg="blue",
    )
    click.secho(
        f"Reading keyfile: {keyfile}",
        err=True,
        bg="white",
        fg="blue",
    )
    passkey = keyfile.read_text().strip()
    client = get_client(username, passkey)

    outdata = []

    for _i, data in get_followers(client, username):
        for d in data:
            outdata.append(d.dict())

        click.secho(
            f"#{_i}: {len(data)} in batch    {len(outdata)} total",
            bg="cyan",
            fg="black",
            err=True,
        )

    click.secho(
        f"{_i} batches  {len(outdata)} total records", bg="black", fg="green", err=True
    )
    outtext = json.dumps(outdata, indent=2)

    click.echo(outtext)


if __name__ == "__main__":
    cli()
