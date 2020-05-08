from io import BytesIO
from zipfile import ZipFile

from Classification_Project.ClassifierFactory import classifier_factory
from Classification_Project.ConsoleLogger import console_logger
from Classification_Project.FileUtils import file_utils


class MethodResultsArchiver:
    def archive_method_results(self, method_name='*'):
        console_logger.info('Archiving started...')

        methods_names = classifier_factory.get_available_classifier_names() if method_name == '*' else [method_name]

        results_to_archive = []

        for method_to_archive_name in methods_names:
            test_predictions_file_path = file_utils.get_session_based_file_path(
                f'{method_to_archive_name}_test_predictions.csv')
            train_predictions_file_path = file_utils.get_session_based_file_path(
                f'{method_to_archive_name}_train_predictions.csv')

            results_to_archive.append((test_predictions_file_path, train_predictions_file_path, method_to_archive_name))

        result = self.__archive_files(results_to_archive)

        console_logger.info('Archiving successfully finished')

        return result

    def __archive_files(self, results):
        memory_file = BytesIO()

        with ZipFile(memory_file, 'w') as archiver:
            for method_results in results:
                archiver.write(method_results[0])
                archiver.write(method_results[1])

        memory_file.seek(0)

        return memory_file
