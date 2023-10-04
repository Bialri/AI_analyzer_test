from dotenv import load_dotenv
import os
from pathlib import Path
import asyncio

from sniffer import Sniffer
from converter import Converter
from handler import Handler

load_dotenv()

BRO_SCRIPT_PATH = os.environ.get('BRO_SCRIPT_PATH')
CONVERT_PATH = os.environ.get('CONVERT_PATH')

MODEL_DIRECTORY_PATH = Path(os.environ.get('MODEL_DIRECTORY_PATH'))
STATUSES_PATH = Path(os.environ.get('STATUSES_PATH'))
Z_SCORE_PATH = Path(os.environ.get('Z_SCORE_PATH'))
MODEL_COLUMNS_PATH = Path(os.environ.get('MODEL_COLUMNS_PATH'))
COLUMN_NAMES_PATH = Path(os.environ.get('COLUMN_NAMES_PATH'))


async def process(converter: Converter, handler: Handler, pcap_file_path):
    converted_file_path = await converter.convert_file(pcap_file_path)
    print(handler.handle_data(converted_file_path))


async def main():
    sniffer = Sniffer()
    converter = Converter(BRO_SCRIPT_PATH, CONVERT_PATH)
    handler = Handler(MODEL_DIRECTORY_PATH, STATUSES_PATH, Z_SCORE_PATH, MODEL_COLUMNS_PATH, COLUMN_NAMES_PATH)

    while True:
        path = await sniffer.create_temp_file()
        asyncio.create_task(process(converter, handler, path))

if __name__ == '__main__':
    asyncio.run(main())