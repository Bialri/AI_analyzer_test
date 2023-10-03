import asyncio
import datetime
import random
from aiofiles.os import mkdir as aiomkdir
import string
from pathlib import Path
import os


class Sniffer:

    @staticmethod
    async def _create_temp_dir():
        path = Path.cwd().joinpath('tmp/')
        if not os.path.exists(path):
            await aiomkdir('./tmp/')
        return path

    async def _create_temp_file_path(self, path):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)) + '.pcap'
        fullpath = path.joinpath(filename)
        if not os.path.exists(path):
            return await self._create_temp_file_path(path)
        return fullpath

    async def create_temp_file(self):
        path = await self._create_temp_dir()
        fullpath = await self._create_temp_file_path(path)
        process = await asyncio.create_subprocess_shell(f'sudo tcpdump -c 50 -w {fullpath}',
                                                        stdout=asyncio.subprocess.PIPE)
        code = await process.wait()
        if code != 0:
            print(code)

        return path


async def print_data(path):
    print(datetime.datetime.now())


async def main():
    sniffer = Sniffer()
    while True:
        try:
            path = await sniffer.create_temp_file()
            asyncio.create_task(print_data(path))
        except KeyboardInterrupt:
            loop = asyncio.get_running_loop()
            loop.stop()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    loop = asyncio.get_running_loop()
    loop.stop()
