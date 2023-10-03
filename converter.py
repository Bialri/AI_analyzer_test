import os
import asyncio
from pathlib import Path, PosixPath
import aiofiles.os as aios


class Converter:

    def __init__(self, bro_script_path: str, convert_path: str) -> None:
        self.bro_script_path = bro_script_path
        self.convert_path = convert_path

    @staticmethod
    def _get_full_file_path(path: PosixPath, filename: str, extention: str) -> PosixPath:
        dir_path_name = path.parent
        filename_with_ext = f'{filename}.{extention}'
        return dir_path_name.joinpath(filename_with_ext)

    @staticmethod
    async def _execute_shell_command(command: str) -> None:
        process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE)
        await process.wait()

    # Note: сделать обработку ошибки при запрете доступа
    @staticmethod
    async def _remove_tmp_file(path: PosixPath) -> None:
        is_exist = await aios.path.exists(path)
        if not is_exist:
            raise OSError('File {path} already deleted')
        try:
            await aios.remove(path)
        except PermissionError:
            raise PermissionError('Permission denied: please ensure that you run program as super user')

    async def _convert_to_list_format(self, path: PosixPath, filename: str) -> PosixPath:
        list_file_path = self._get_full_file_path(path, filename, 'list')
        command = f'sudo bro -r {path} {self.bro_script_path} > {list_file_path}'
        await self._execute_shell_command(command)

        return list_file_path

    async def _sort_list_file(self, list_path: PosixPath, filename: str) -> PosixPath:
        sorted_filename = f'{filename}_sorted'
        sorted_file_path = self._get_full_file_path(list_path, sorted_filename, 'list')
        command = f'sudo sort -n {list_path} > {sorted_file_path}'
        await self._execute_shell_command(command)

        return sorted_file_path

    async def _convert_to_output_format(self, list_sorted_path: PosixPath, filename: str) -> PosixPath:
        list_output_filename = f'{filename}_output'
        list_output_path = self._get_full_file_path(list_sorted_path, list_output_filename, '.list')
        command = f'sudo {self.convert_path} {list_sorted_path} {list_output_path}'
        await self._execute_shell_command(command)

        return list_output_path

    async def convert_file(self, path: PosixPath) -> PosixPath:
        filename = str(os.path.basename(path).split('.')[0])
        list_file_path = await self._convert_to_list_format(path, filename)
        await self._remove_tmp_file(path)
        list_sort_file_path = await self._sort_list_file(list_file_path,filename)
        await self._remove_tmp_file(list_file_path)
        list_output_file = await self._convert_to_output_format(list_sort_file_path,filename)
        await self._remove_tmp_file(list_sort_file_path)

        return list_output_file


async def main():
    path = Path.cwd().joinpath('tmp/P4CE56M12LB75384UOL7.pcap')
    converter = Converter(bro_script_path='fgfgfgffg', convert_path='fdfdfdfdfd')
    await converter.convert_file(path)


asyncio.run(main())
