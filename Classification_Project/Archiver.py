from io import BytesIO
from zipfile import ZipFile

from Classification_Project.ConsoleLogger import console_logger
from Classification_Project.FileUtils import file_utils


class Archiver:
    def archive_session_based_files(self):
        console_logger.info('Archiving started...')

        test_predictions_file_path = file_utils.get_session_based_file_path('test_predictions.csv')
        train_predictions_file_path = file_utils.get_session_based_file_path('train_predictions.csv')

        result = self.__archive_files([test_predictions_file_path, train_predictions_file_path])

        console_logger.info('Archiving successfully finished')

        return result

    def __archive_files(self, tmp_file_paths):
        memory_file = BytesIO()

        with ZipFile(memory_file, 'w') as archiver:
            for path in tmp_file_paths:
                archiver.write(path)

        memory_file.seek(0)

        return memory_file
