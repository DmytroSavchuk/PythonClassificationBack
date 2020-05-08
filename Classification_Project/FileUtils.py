import io
import os
from pathlib import Path

import numpy as np

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.ClassifierFactory import classifier_factory
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

    def is_classification_result_files_exists(self, method_name='*'):
        if method_name == '*':
            for method_name in classifier_factory.get_available_classifier_names():
                if (not Path(self.get_session_based_file_path(f'{method_name}_test_predictions.csv')).is_file()) or \
                        (not Path(self.get_session_based_file_path(f'{method_name}_train_predictions.csv')).is_file()):
                    return False

            return True

        return Path(self.get_session_based_file_path(f'{method_name}_test_predictions.csv')).is_file() and Path(
            self.get_session_based_file_path(f'{method_name}_train_predictions.csv')).is_file()

    def get_session_based_file_path(self, file_name):
        return '{}/{}_{}'.format(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'),
                                 session_service.get_session_id(), file_name)

    def is_file_for_session(self, file_name):
        if Path(self.get_session_based_file_path(file_name)).is_file():
            return True
        return False

    def read_file(self, filepath, delete_after_read=False):
        file = io.BytesIO()
        with open(filepath, 'rb') as fo:
            file.write(fo.read())

        file.seek(0)

        if delete_after_read:
            os.remove(filepath)

        return file


file_utils = FileUtils()
