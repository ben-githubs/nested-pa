#! /opt/homebrew/bin/python3

from github import Github, Auth
from uuid import uuid4

from dotenv import load_dotenv
import os

load_dotenv(".env")

def make_release():
    auth = Auth.Token(os.environ.get("GH_TOKEN"))
    g = Github(auth=auth)

    repo = g.get_repo('ben-githubs/upstream-test')
    contents = repo.get_contents("test.txt")
    result = repo.update_file(contents.path, "Version bump", str(uuid4()), contents.sha, branch="main")
    commit = result['commit']

    version = "v0.0.0"
    try:
        last_release = repo.get_latest_release()
        version = last_release.tag_name
        version_parts = version.split('.')
        minor = int(version_parts[1])
        version_parts[1] = str(minor + 1)
        version = '.'.join(version_parts)
    except:
        pass


    repo.create_git_tag(
        version,
        "New release",
        commit.sha,
        "commit"
    )

    repo.create_git_release(
        version, # tag
        "New release", # name
        "New release", # message
    )

if __name__ == "__main__":
    make_release()