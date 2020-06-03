import io
import os
import pickle
import shutil
import uuid
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

from Classification_Project.ApplicationConstants import ApplicationConstants
from Classification_Project.ClassifierFactory import classifier_factory
from Classification_Project.ConsoleLogger import console_logger
from Classification_Project.Data import Data
from Classification_Project.ImageUtils import image_utils
from Classification_Project.SessionService import *


class FileUtils:
    def save_session_based_image_data(self, archive, archive_name, file_name):
        self.save_session_based_file(archive, archive_name)

        images_path = self.__extract_image_data(self.get_session_based_file_path(archive_name))
        self.__resize_images(images_path)

        self.__generate_image_dataset_file(images_path, file_name)

        shutil.rmtree(images_path)
        os.remove(self.get_session_based_file_path(archive_name))

    def __extract_image_data(self, archive_path):
        tmp_images_path = f'{ApplicationConstants.get_constant("UPLOADS_FOLDER_PATH")}/{uuid.uuid1()}'

        with zipfile.ZipFile(archive_path, 'r') as zipObj:
            zipObj.extractall(tmp_images_path)

        return tmp_images_path

    def __resize_images(self, tmp_images_path):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(tmp_images_path):
            for f in filenames:
                files.append(f'{dirpath}/{f}')

        for file_name in files:
            self.__resize_image(file_name)

    def __resize_image(self, image_path):
        img = Image.open(image_path)
        img = img.resize((ApplicationConstants.get_constant('CLASSIFICATION_IMAGE_WIDTH'),
                          ApplicationConstants.get_constant('CLASSIFICATION_IMAGE_HEIGHT')), Image.ANTIALIAS)
        img.save(image_path)

        return img

    def __generate_image_dataset_file(self, images_path, file_name):
        x = []
        y = []

        for (dirpath, dirnames, filenames) in os.walk(images_path):
            for f in filenames:
                x.append(image_utils.flatten_image_array(image_utils.convert_image_to_np_array(f'{dirpath}/{f}')))
                y.append(Path(f'{dirpath}/{f}').parent.name)

        self.save_session_based_object(Data(x, y), file_name)

    def save_session_based_file(self, file, file_name=''):
        if not Path(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')).is_dir():
            os.mkdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))

        file_path = self.get_session_based_file_path(file_name)

        file.save(file_path)

    def numpy_save_session_based_txt_file(self, file, file_name=''):
        if not Path(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')).is_dir():
            os.mkdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))

        file_path = self.get_session_based_file_path(file_name)

        np.savetxt(file_path, file, fmt="%s")

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

    def delete_user_files(self, pattern='*'):
        if os.path.exists(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')):
            if pattern == '*':
                console_logger.info("Clearing tmp folder...")

                shutil.rmtree(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))
                os.mkdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))
            else:
                for file_name in self.get_user_files_names(pattern):
                    os.remove(f'{ApplicationConstants.get_constant("UPLOADS_FOLDER_PATH")}/{file_name}')

    def get_user_files_names(self, pattern='*'):
        if os.path.exists(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH')):
            if pattern == '*':
                return os.listdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))

            return list(filter(lambda f: pattern in f,
                               os.listdir(ApplicationConstants.get_constant('UPLOADS_FOLDER_PATH'))))

        return []

    def save_session_based_object(self, object_to_save, file_name):
        file_path = self.get_session_based_file_path(file_name)

        pickle.dump(object_to_save, open(file_path, 'wb'), pickle.HIGHEST_PROTOCOL)

    def get_session_based_object(self, file_name):
        file_path = self.get_session_based_file_path(file_name)

        return pickle.load(open(file_path, 'rb'))


file_utils = FileUtils()
