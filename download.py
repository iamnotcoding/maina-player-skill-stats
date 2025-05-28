from http import HTTPStatus
import asyncio
from typing import Any
import requests
from urllib.parse import unquote

BASE_URL = "https://txy1.sayobot.cn"


def get_file_name_from_header(headers: dict[str, str]) -> str:
    '''
    Returns a unquoted file name from a https header
    '''
    line = headers["content-disposition"]
    chunk = line.split(";")[1]

    return unquote(chunk.split('"')[1].split('"')[0])


async def download_beatmapset(
    beatmapset_id: int, directory_path: str
) -> tuple[bool, str]:
    """
    Returns True and the file name if succeeded, otherwise false
    """
    url = f"{BASE_URL}/beatmaps/download/full/{beatmapset_id}?server=auto"

    response = requests.get(url=url, allow_redirects=True, timeout=600)

    if response.status_code != HTTPStatus.OK:
        print(f"Downloading a beaetmapset failed : {response.status_code}")

        try:
            file_name = get_file_name_from_header(dict(response.headers))
        except Exception:
            return False, f"id : {beatmapset_id}"
        
        return False, file_name

    file_name = get_file_name_from_header(dict(response.headers))

    with open(f"{directory_path}/{file_name}", "wb+") as file:
        file.write(response.content)

    return True, file_name


async def download_beatmapsets(beatmapset_ids: list[int], directory_path: str, concurrent_count : int = 4) -> None:
    """
    Calls download_beatmapset()s
    """
    def done_callback(t : Any) -> None:
        nonlocal tasks

        status, file_name = t.result()

        if status:
            print(f"Successfully downloaded the map : {file_name}")
        else:
            print(f"Failed to download the map : {file_name}")
        tasks.discard(t)

    tasks: set[Any] = set()
    i = 0

    while len(beatmapset_ids) - concurrent_count
        for beatmapset_id in beatmapset_ids[i : i+concurrent_count]:
            print(f'test : {beatmapset_id}')
            task = asyncio.create_task(download_beatmapset(beatmapset_id, directory_path))
            tasks.add(task)
            task.add_done_callback(done_callback)

        await asyncio.gather(*tasks)
        print('group ended')

    if len(beatmapset_ids) - concurrent_count > 0:
        i += concurrent_count

    for beatmapset_id in beatmapset_ids[i:]:
        print(beatmapset_id)
        task = asyncio.create_task(download_beatmapset(beatmapset_id, directory_path))
        tasks.add(task)
        task.add_done_callback(
            lambda t: (print(
                ("Successfully downloaded the map"
                if t.result()[0]
                else "Failed to download the map") + f" : {t.result()[1]}"
            ), tasks.discard(t))
        )

    await asyncio.gather(*tasks)


asyncio.run(download_beatmapsets([i for i in range(17)], "./beatmapsets"))
