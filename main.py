import os
import json
import requests
import asyncio
from typing import Any

import api_util
import download

def get_only_4k_maps(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:
    '''
    Excludes maps which have a key mode other than the 4k
    '''
    return [score for score in scores if score['beatmap']['cs'] == 4]


def main():
    print('Loading settings.json')
    settings = json.load(open('settings.json', 'r', encoding='UTF-8'))
    settings['client_id'] = int(settings['client_id']) # since it might be a string

    print('Getting the access token')
    acess_token = api_util.authenticate(settings['client_id'], settings['client_secret'])

    print('Getting 4k scores out of your best, recent, first place scores')
    all_scores = api_util.get_user_scores(settings['user_id'], acess_token)
    scores_4k = get_only_4k_maps(all_scores)

    print(f'The total number of 4k scores : {len(scores_4k)}')

    beatmapset_ids : list[int] = [score_4k["beatmap"]["beatmapset_id"] for score_4k in scores_4k]
    print(beatmapset_ids)
    print('Downloading all the beatmapsets')
    asyncio.run(download.download_beatmapsets(beatmapset_ids, "./beatmapsets"))

if __name__ == "__main__":
    main()