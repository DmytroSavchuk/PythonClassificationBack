import os
from pathlib import Path

from flask import session

from Classification_Project.ApplicationConstants import ApplicationConstants


class FileUtils:
    def save_session_based_txt_file(self, file, file_name=''):
        if not Path(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')).is_dir():
            os.mkdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))

        file_path = '{}/{}_{}.txt'.format(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'),
                                          session.get('session_id'), file_name)

        file.save(file_path)

    def get_session_based_file_path(self, file_name):
        return '{}/{}_{}.txt'.format(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'),
                                     session.get('session_id'), file_name)

    def is_file_for_session(self, file_name):
        if Path('{}/{}_{}.txt'.format(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'),
                                      session.get('session_id'), file_name)).is_file():
            return True
        return False
