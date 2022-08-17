from __future__ import annotations

import json
import os
import sys
import time
from typing import Any
from urllib.request import Request
from urllib.request import urlopen

GITHUB_BASE_URL: str = "https://api.github.com/{endpoint}"
GITHUB_CHECK_RUNS_IN_REPOSITORY_ENDPOINT: str = (
    "repos/{repository}/commits/{ref}/check-runs"
)
GITHUB_CHECK_RUN_BY_ID_ENDPOINT: str = "repos/{repository}/check-runs/{id}"

ENV_VARS = {
    "REF": "",
    "REPOSITORY": "",
    "GH_TOKEN": "",
    "CHECK_NAMES": [],
    "ALLOWED_STATES": [],
    "MAX_WAIT_TIME": "",
}
# override defaults with environment variables
for env, default in ENV_VARS.items():
    if env in ("CHECK_NAMES", "ALLOWED_STATES"):
        ENV_VARS[env] = (
            os.getenv(env).split(";")
            if ";" in os.getenv(env)
            else os.getenv(env, default)
        )
    else:
        ENV_VARS[env] = os.getenv(env, default)


def _make_github_request(endpoint: str, token: str) -> dict[Any, Any]:
    url = Request(
        GITHUB_BASE_URL.format(endpoint=endpoint),
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {token}",
        },
    )

    with urlopen(url) as response:
        return json.loads(response.read())


def _get_checks_in_repository(
    repository: str,
    ref: str,
    token: str,
) -> list[dict[str, Any]] | None:
    """ """
    endpoint = GITHUB_CHECK_RUNS_IN_REPOSITORY_ENDPOINT.format(
        repository=repository,
        ref=ref,
    )
    body = _make_github_request(endpoint=endpoint, token=token)
    if "total_count" in body:
        if int(body["total_count"]) > 0:
            return body["check_runs"]

    return None


def _get_check_status(
    repository: str,
    checks: list[dict[str, Any]],
    allowed_states: list[str],
    token: str,
) -> bool:
    """ """
    list_of_status = []
    for check in checks:
        endpoint = GITHUB_CHECK_RUN_BY_ID_ENDPOINT.format(
            repository=repository,
            id=check["id"],
        )
        body = _make_github_request(endpoint=endpoint, token=token)
        list_of_status.append(body["status"])

    return all(status in allowed_states for status in list_of_status)


def main():
    """ """
    max_wait_time = int(ENV_VARS["MAX_WAIT_TIME"])
    elapsed_time = 0

    print(f"Using ref: {ENV_VARS['REF']}")
    print(f"Using repository: {ENV_VARS['REPOSITORY']}")
    if isinstance(ENV_VARS["CHECK_NAMES"], list):
        print(f"Using checkNames: {','.join(ENV_VARS['CHECK_NAMES'])}")
    else:
        print(f"Using checkNames: {ENV_VARS['CHECK_NAMES']}")

    if isinstance(ENV_VARS["ALLOWED_STATES"], list):
        print(f"Using allowedStates: {','.join(ENV_VARS['ALLOWED_STATES'])}")
    else:
        print(f"Using allowedStates: {ENV_VARS['ALLOWED_STATES']}")

    while elapsed_time <= max_wait_time:
        print(
            f"Remaining time in seconds until failure: {max_wait_time - elapsed_time} seconds",
        )
        all_checks_in_repo = _get_checks_in_repository(
            repository=ENV_VARS["REPOSITORY"],
            ref=ENV_VARS["REF"],
            token=ENV_VARS["GH_TOKEN"],
        )

        if not all_checks_in_repo:
            print("Couldn't find any checks for current ref.")
            print("::set-output name=status::failed")
            return 1

        checks = [
            check
            for check in all_checks_in_repo
            if check["name"] in ENV_VARS["CHECK_NAMES"]
        ]

        status = _get_check_status(
            repository=ENV_VARS["REPOSITORY"],
            checks=checks,
            allowed_states=ENV_VARS["ALLOWED_STATES"],
            token=ENV_VARS["GH_TOKEN"],
        )

        if status:
            print("Completed the check validation successfully.")
            print("::set-output name=status::success")
            break

        print(
            f"Not all checks are in an allowed state ({ENV_VARS['ALLOWED_STATES']}). Waiting 5 seconds.",
        )
        elapsed_time += 5
        time.sleep(5)
    else:
        print("Reached wait time limit.")
        print("::set-output name=status::false")

    return 0


if __name__ == "__main__":
    sys.exit(main())
