#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

import requests
import re
import os
import sys
import argparse

SLACK_API_TOKEN_REGEX = r"(xoxc-[a-zA-Z0-9-]+)"
SEARCH_FILES_URL = "https://slack.com/api/search.files"
MAX_RESULT_COUNT = 100


def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="slack-image-dump.py",
        description="Commandline tool to dump slack images from a workspace based on a specified query",
        epilog="slack-image-dump expects a cookie supplied with the -c parameter or set with the environment variable SLACK_COOKIE",
    )
    parser.add_argument(
        "-q", "--query", required=True, help="Slack keyword search query"
    )
    parser.add_argument(
        "-w", "--workspace", required=True, help="Slack workspace url to search"
    )
    parser.add_argument(
        "-c",
        "--cookie",
        required=False,
        help="Slack d cookie extracted from a browser session (starting with `xoxd-`)",
    )
    parser.add_argument(
        "-u", "--user-agent", required=False, help="Optional User-Agent override"
    )

    return parser


class SlackImageDump:
    def __init__(
        self, workspace_url: str, cookie: str, user_agent: str | None = None
    ) -> None:
        self.s = requests.Session()

        # normalize workspace_url
        self.workspace_url = workspace_url
        if not self.workspace_url.startswith("https://"):
            self.workspace_url = f"https://{self.workspace_url}"
        if not self.workspace_url.endswith(".slack.com"):
            self.workspace_url = f"{self.workspace_url}.slack.com"

        # set cookie
        self.s.cookies.update({"d": cookie})

        # get token from cookie
        token = self._get_token()

        # set authentication and user-agent headers
        headers = {}
        if user_agent is not None:
            headers["User-Agent"] = user_agent
        headers["Authorization"] = f"Bearer {token}"
        self.s.headers.update(headers)

    def _get_token(self) -> None:
        r = None
        try:
            r = self.s.get(
                self.workspace_url,
            ).text
            tokens = list(set(re.findall(SLACK_API_TOKEN_REGEX, r)))

            if len(tokens) >= 1:
                return tokens[0]
            else:
                print(
                    f"Error: No Slack tokens found. Ensure that the supplied cookie is valid for the specified workspace ({self.workspace_url}). "
                    "If this is an enterprise Slack account, you might need to supply the workspace url as workspacename.enterprise.slack.com."
                )
                sys.exit(1)
        except requests.RequestException as e:
            print(f"Error: {e}")
            sys.exit(1)

    def dump_images(self, query: str) -> None:
        path = query.replace(" ", "-").replace('"', "").replace("'", "")
        path = f"./slack-image-dump-{path}"
        try:
            os.mkdir(path)
        except FileExistsError as e:
            print(f"Error: {e}")
            sys.exit(1)

        if not "type:images" in query:
            query = f"{query} type:images"

        matches = []
        page = 1
        pages = MAX_RESULT_COUNT
        while page <= pages:
            r = self.s.get(
                SEARCH_FILES_URL,
                params=dict(query=query, count=MAX_RESULT_COUNT, page=page),
            ).json()
            if r["ok"] == True:
                page = r["files"]["paging"]["page"] + 1
                pages = r["files"]["paging"]["pages"]
                matches.extend(r["files"]["matches"])
            else:
                print(f"Error: {r.text}")
                sys.exit(1)

        counter = 0
        total = len(matches)
        for file in matches:
            bar = int((counter / total) * 50)
            space = 50 - bar
            print(
                f"Progress: [ {'='*bar}>{' '*space} ] ({counter} / {total}) files",
                end="\r",
            )
            r = self.s.get(
                file["url_private_download"],
            )

            with open(f"{path}/{counter}.png", "wb") as f:
                f.write(r.content)
            counter += 1


if __name__ == "__main__":
    args = cli().parse_args()
    cookie = args.cookie
    if args.cookie is None:
        cookie = os.environ.get("SLACK_COOKIE")
        if cookie is None:
            print(
                "Error: a cookie value must be supplied via the -c paramater or as an environment variable (SLACK_COOKIE)"
            )
            sys.exit(1)

    sid = SlackImageDump(
        workspace_url=args.workspace, cookie=cookie, user_agent=args.user_agent
    )
    sid.dump_images(query=args.query)
