#!/usr/bin/env python3
from pathlib import Path

import argparse
import hashlib
import os
import sys

try:
    import requests
except ModuleNotFoundError:
    print("Missing module request, install with\n\n  $ sudo dnf install python3-requests\n")
    sys.exit(1)

try:
    import yaml
except ModuleNotFoundError:
    print("Missing module yaml, install with\n\n  $ sudo dnf install python3-pyyaml\n")
    sys.exit(1)


root_path = Path(__file__).parent.parent


def fetch_file(url, filepath):
    if filepath.is_file():
        print(f"File {filepath.name} already downloaded")
        return

    print(f"Fetching {filepath.name} from {url}")
    with requests.get(url, stream=True) as req:
        req.raise_for_status()
        with open(filepath, 'wb') as fd:
            for chunk in req.iter_content(chunk_size=16384):
                fd.write(chunk)


def verify_file(filepath, oid, oid_type):
    if oid_type == 'sha256':
        hasher = hashlib.sha256()
    else:
        print(f"Unsupported oid_type: {oid_type}")
        sys.exit(1)

    with open(filepath, "rb") as fd:
        for chunk in iter(lambda: fd.read(16384), b""):
            hasher.update(chunk)

    if hasher.hexdigest() != oid:
        print(f"Checksum missmatch for {filepath.name}")
        return False
    return True


args = {}
def parse_args():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Relative path to 3pp directory")
    args = parser.parse_args()


def main():
    success = True
    parse_args()
    tpp_path = root_path / args.path

    for file in yaml.safe_load((tpp_path / 'files').read_text())['files']:
        fetch_file(file['url'], tpp_path / file['name'])
        if not verify_file(tpp_path / file['name'], file['oid'], file['oid_type']):
            success = False

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
