from enum import Enum


class ApplicationConstants(Enum):
    CLIENT_HOST = '*'  # todo Should be replace with client host on Master branch
    LOCAL_CLIENT_HOST = 'http://localhost:4200'
    APP_SECRET_KEY = 'e8fd411b86609d1b6416e1e3da69ab27'
    AVAILABLE_CLASSIFICATION_METHODS_FOLDER_PATH = 'Classification_Project/resources/classification_methods'
