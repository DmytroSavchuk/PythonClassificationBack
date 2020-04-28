import os

LOCAL_CLIENT_HOST = 'http://localhost:4200'
CLIENT_HOST = '*'  # todo Should be replace with client host on Master branch

is_production = True if os.environ['IS_PRODUCTION'] == 'True' else False
APP_SECRET_KEY = 'e8fd411b86609d1b6416e1e3da69ab27'

CONSTANTS_MAP = {
    'CLIENT_HOST': CLIENT_HOST if is_production else LOCAL_CLIENT_HOST,
    'APP_SECRET_KEY': 'e8fd411b86609d1b6416e1e3da69ab27',
    'AVAILABLE_CLASSIFICATION_METHODS_FOLDER_PATH': 'Classification_Project/resources/classification_methods'
    if is_production else 'resources/classification_methods',
    'UPLOADS_FOLDER_PATH': 'Classification_Project/resources/uploads' if is_production else 'resources/uploads',
    'SESSION_TTL': 3 * 60 * 60 * 1000
}


class ApplicationConstants:
    @staticmethod
    def get_constant(key):
        try:
            return CONSTANTS_MAP[key]
        except KeyError:
            raise Exception(f"There is no such key {key}")
