import os
from pathlib import Path

import numpy as np

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.SessionService import *


class FileUtils:
    def save_session_based_txt_file(self, file, file_name=''):
        if not Path(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')).is_dir():
            os.mkdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))

        file_path = self.get_session_based_file_path(file_name)

        file.save(file_path)

    def numpy_save_session_based_txt_file(self, file, file_name=''):
        if not Path(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')).is_dir():
            os.mkdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))

        file_path = self.get_session_based_file_path(file_name)

        np.savetxt(file_path, file)

    def get_session_based_file_path(self, file_name):
        return '{}/{}_{}'.format(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'),
                                 session_service.get_session_id(), file_name)

    def is_file_for_session(self, file_name):
        if Path(self.get_session_based_file_path(file_name)).is_file():
            return True
        return False


file_utils = FileUtils()
