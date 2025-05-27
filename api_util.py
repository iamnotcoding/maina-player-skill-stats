'''
This module defines wrapper functions for osu API
'''

from typing import Any
import json
from http import HTTPStatus
import requests

BASE_URL = "https://osu.ppy.sh/api/v2"


def authenticate(client_id: int, client_secret: str) -> str:
    """
    Authenticates with the osu! API using client credentials.
    Returns status code and access token.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data: dict[str, Any] = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": "public",
    }

    response = requests.post(
        "https://osu.ppy.sh/oauth/token", headers=headers, data=data, timeout=30
    )

    if response.status_code != HTTPStatus.OK:
        raise ConnectionRefusedError(f"Failed to authenticate : {response.status_code}")

    return response.json()["access_token"]


def get_user_scores(user_id: int, token: str) -> list[dict[str, Any]]:
    """
    Fetches user data from the osu! API.
    Returns the scores
    """

    score_types = ["best", "recent", "firsts"]
    scores: list[dict[str, Any]] = []

    for score_type in score_types:
        url = f"{BASE_URL}/users/{user_id}/scores/{score_type}?mode=mania&limit=100"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != HTTPStatus.OK:
            raise ConnectionRefusedError(f"Failed to fetch user scores: {response.status_code}")

        scores += list(response.json())

    return scores

if __name__ == "__main__":
    json_data = json.load(open("settings.json", "r", encoding="utf-8"))

    access_token = authenticate(
        json_data["client_id"], json_data["client_secret"]
    )

    print(f"Access Token: {access_token}")

    scores = get_user_scores(17770010, access_token)
    scores_4k = get_only_4k_maps(scores)

    print(f"User Data: {json.dumps(scores[0])}")
    print(f"Number of scores fetched: {len(scores_4k)}")
