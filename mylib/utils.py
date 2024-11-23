from pathlib import Path
import yaml

DEFAULT_BSKY_KEYFILE_PATH = Path("~/.bskyrc").expanduser()


def get_passkey(username: str, keyfile: [str, Path] = DEFAULT_BSKY_KEYFILE_PATH) -> str:
    with open(keyfile, "r") as kfile:
        return yaml.safe_load(kfile)[username]
