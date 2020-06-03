import uuid
import zipfile

import pandas as pd
from PIL import Image

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.Data import Data
from Classification_Project.FileUtils import FileUtils


class DataExtractor:
    def __init__(self):
        self.file_utils = FileUtils()

    def extract_data(self, file_name):
        extracted_data = pd.read_csv(self.file_utils.get_session_based_file_path(file_name), header=None)

        return Data(extracted_data.iloc[:, :-1], extracted_data.iloc[:, -1])

    def extract_image_data(self, archive_name):
        tmp_images_path = f'{ApplicationConstants.get_constant("UPLOADS_FOLDER_PATH")}/{uuid.uuid1()}'
        archive_path = self.file_utils.get_session_based_file_path(archive_name)

        with zipfile.ZipFile(archive_path, 'r') as zipObj:
            zipObj.extractall(tmp_images_path)

    def __resize_image(image_path, result_path):
        img = Image.open(image_path)
        img = img.resize((ApplicationConstants.get_constant('CLASSIFICATION_IMAGE_WIDTH'),
                          ApplicationConstants.get_constant('CLASSIFICATION_IMAGE_HEIGHT')), Image.ANTIALIAS)
        img.save(result_path)

        return img
