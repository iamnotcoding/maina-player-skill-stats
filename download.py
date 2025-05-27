"""
This module downloads maps by using osynic
"""

import os
import tempfile
import json
from subprocess import Popen, PIPE, STDOUT
import asyncio
import time


async def download_beatmapset(beatmapset_id: int, directory_path: str) -> None:
    """
    Downloads a beatmapset using osynic
    """
    d = {"beatmapset_ids": [str(beatmapset_id)]}
    print(d)
    with tempfile.NamedTemporaryFile("w", encoding="UTF-8", delete=False) as file:
        json.dump(d, file, indent=4)

        file_name = file.name

    try:
        process = Popen(
            ["./osynic-dl.exe", "-b", file_name, "-o", directory_path],
            stdout=PIPE,
            stderr=STDOUT,
        )

        while True:
            line = process.stdout.readline()

            print(line)

            if line.find(b"0") != -1:
                process.kill()
                break

        process.wait()
    finally:
        for _ in range(5):
            try:
                os.remove(file_name)
                break
            except PermissionError:
                time.sleep(0.5)
        else:
            print(f"Warning: could not delete temp file {file_name}")


async def download_beatmapsets(beatmapset_ids: list[int], directory_path: str) -> None:
    """
    Calls download_beatmapset() asynchronously
    """
    async with asyncio.TaskGroup() as tg:
        for beatmapset_id in beatmapset_ids:
            tg.create_task(download_beatmapset(beatmapset_id, directory_path))
