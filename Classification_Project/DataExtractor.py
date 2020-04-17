import pandas as pd

from Classification_Project.Data import Data
from Classification_Project.FileUtils import FileUtils


class DataExtractor:
    def __init__(self):
        self.file_utils = FileUtils()

    def extract_data(self, file_name):
        extracted_data = pd.read_csv(self.file_utils.get_session_based_file_path(file_name), header=None)

        return Data(extracted_data.iloc[:, :-1], extracted_data.iloc[:, -1])
