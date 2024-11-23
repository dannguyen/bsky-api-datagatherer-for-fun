#!/usr/bin/env python3
from click_default_group import DefaultGroup
from rich_click import RichGroup
from mylib import protocol as myproto
from mylib.utils import get_passkey, DEFAULT_BSKY_KEYFILE_PATH

"""
https://docs.bsky.app/docs/api/app-bsky-graph-get-followers
TODO:
hydrate follower counts and other metrics
get common followers?
"""


from pathlib import Path
from atproto import Client
import rich_click as click
import json


class DefaultRichGroup(DefaultGroup, RichGroup):
    """Make `click-default-group` work with `rick-click`."""


COMMON_CLICK_FLAGS = {
    "username": click.option(
        "--username",
        "-u",
        default="dancow.bsky.social",
        help=f"A bluesky user handle, domain and all, e.g. jay.bsky.app",
        required=False,
        show_default=True,
        type=click.STRING,
    ),
    "keyfile": click.option(
        "--keyfile",
        "-k",
        default=DEFAULT_BSKY_KEYFILE_PATH,
        help=f"The file path where the bluesky yaml username:passkey pair values exist",
        required=False,
        show_default=True,
        type=click.Path(dir_okay=False, path_type=Path, resolve_path=True, exists=True),
    ),
    "output-path": click.option(
        "--output-path",
        "-o",
        default="-",
        help=f"Set the path of the output file. Default is printing to stdout.",
        required=False,
        show_default=False,
        type=click.Path(dir_okay=False, path_type=Path, resolve_path=True),
    ),
}


### decorators
def shared_client_opts(fn):
    for oname in (
        "username",
        "keyfile",
    ):
        fn = COMMON_CLICK_FLAGS[oname](fn)
    return fn


def init_client(username, keyfile):
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
    passkey = get_passkey(username, keyfile)
    client = myproto.get_client(username, passkey)
    return client


@click.version_option()
@click.group(cls=DefaultRichGroup, default="me", default_if_no_args=True)
def cli():
    pass


@cli.command()
@shared_client_opts
def me(username, keyfile):
    client = init_client(username, keyfile)
    data = json.dumps(client.me.dict(), indent=2)
    click.echo(data)


############## get followers


@cli.command()
@shared_client_opts

# @click.
def followers(username, keyfile, output_path):
    client = init_client(username, keyfile)
    outdata = []

    try:
        for _i, data in myproto.get_followers(client, username):
            for d in data:
                outdata.append(d.dict())

            click.secho(
                f"#{_i}: {len(data)} in batch    {len(outdata)} total",
                bg="cyan",
                fg="black",
                err=True,
            )
    except Exception as e:
        raise click.UsageError(f"An error occurred: {str(e)}")

    click.secho(
        f"{_i} batches  {len(outdata)} total records", bg="black", fg="green", err=True
    )

    outtext = json.dumps(outdata, indent=2)
    click.echo(outtext)


if __name__ == "__main__":
    cli()
