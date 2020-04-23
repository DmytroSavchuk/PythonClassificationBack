import os
from pathlib import Path

from flask import session


class FileUtils:
    def save_session_based_txt_file(self, file, file_name=''):
        if not Path('resources/uploads').is_dir():
            os.mkdir('resources/uploads')

        file_path = 'resources/uploads/{}_{}.txt'.format(session.get('session_id'), file_name)

        file.save(file_path)

    def get_session_based_file_path(self, file_name):
        return 'resources/uploads/{}_{}.txt'.format(session.get('session_id'), file_name)

    def is_file_for_session(self, file_name):
        if Path('resources/uploads/{}_{}.txt'.format(session.get('session_id'), file_name)).is_file():
            return True
        return False
