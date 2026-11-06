"""Publish prebuilt canonical skill assets using this public repository's GITHUB_TOKEN."""

import hashlib
import json
import os
from pathlib import Path
import subprocess

def gh(*args):
    return subprocess.check_output(['gh', *args])


def publish(folder: Path, files: dict[str, bytes], version: str, repository: str):
    # Published release assets must be locked by GitHub, not just named after a version.
    releases = json.loads(gh('api', '--paginate', '--slurp', f'repos/{repository}/releases?per_page=100'))
    release = next((item for page in releases for item in page if item['tag_name'] == f'v{version}'), None)
    if release and not release['draft']:
        if not release.get('immutable'):
            raise SystemExit('Existing release is mutable; use a new version with immutable releases enabled')
        expected = {name: f'sha256:{hashlib.sha256(data).hexdigest()}' for name, data in files.items()}
        actual = {asset['name']: asset.get('digest') for asset in release['assets']}
        if any(actual.get(name) != digest for name, digest in expected.items()):
            raise SystemExit('Published assets differ or are missing; bump the plugin version')
        return
    if not release:
        gh('release', 'create', f'v{version}', '--repo', repository, '--verify-tag', '--draft',
           '--title', f'SimpleVox {version}', '--notes', 'Shared SimpleVox agent skills with references and SHA-256 discovery index.')
    # Only drafts can be repaired on retry; published assets are never overwritten.
    gh('release', 'upload', f'v{version}', '--repo', repository, '--clobber',
       *(str(folder / name) for name in files))
    gh('release', 'edit', f'v{version}', '--repo', repository, '--draft=false')
    published = json.loads(gh('api', f'repos/{repository}/releases/tags/v{version}'))
    if not published.get('immutable'):
        raise SystemExit('Release was not made immutable; do not promote its discovery index')


def main():
    root = Path(__file__).resolve().parent.parent
    version = json.loads((root / 'version.json').read_text())['version']
    if os.environ.get('RELEASE_TAG') != f'v{version}':
        raise SystemExit('Release tag must match version.json')
    repository = os.environ.get('GITHUB_REPOSITORY', '')
    if repository != 'simplevox/simplevox-skills':
        raise SystemExit('This workflow only publishes simplevox/simplevox-skills')
    folder = root / 'release-assets'
    files = {path.name: path.read_bytes() for path in folder.iterdir() if path.is_file()}
    index = json.loads(files['agent-skills-index.json'])
    for skill in index['skills']:
        filename = f"{skill['name']}-{version}.tar.gz"
        expected = f'https://github.com/{repository}/releases/download/v{version}/{filename}'
        if skill['url'] != expected or skill['digest'] != f"sha256:{hashlib.sha256(files[filename]).hexdigest()}":
            raise SystemExit('Release index and prebuilt archives do not match')
    publish(folder, files, version, repository)


if __name__ == '__main__':
    main()
