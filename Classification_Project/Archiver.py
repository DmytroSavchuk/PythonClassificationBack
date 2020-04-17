import os
import uuid
from io import BytesIO
from zipfile import ZipFile

import numpy as np


class Archiver:
    def archive(self, *args):
        tmp_file_paths = []

        for arg in args:
            tmp_file_paths.append(self.__save_tmp_file(arg))

        result = self.__archive_temp_files(tmp_file_paths)

        self.__remove_tmp_files(tmp_file_paths)

        return result

    def __save_tmp_file(self, content):
        file_path = 'resources\\tmp\\' + str(uuid.uuid1()) + '.csv'

        np.savetxt(file_path, content)

        return file_path

    def __archive_temp_files(self, tmp_file_paths):
        memory_file = BytesIO()

        with ZipFile(memory_file, 'w') as archiver:
            for path in tmp_file_paths:
                archiver.write(path)

        memory_file.seek(0)

        return memory_file

    def __remove_tmp_files(self, tmp_file_paths):
        for path in tmp_file_paths:
            os.remove(path)
