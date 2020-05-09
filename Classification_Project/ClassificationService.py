import json

from werkzeug.exceptions import BadRequest

from Classification_Project.ClassificationMethodReader import ClassificationMethodReader, classification_method_reader
from Classification_Project.ClassificationResponseDto import ClassificationResponseDto
from Classification_Project.ClassifierEngine import ClassifierEngine
from Classification_Project.ClassifierFactory import ClassifierFactory
from Classification_Project.ConsoleLogger import console_logger
from Classification_Project.DataExtractor import DataExtractor
from Classification_Project.DefaultClassificationResponseDto import DefaultClassificationResponseDto
from Classification_Project.FileUtils import file_utils
from Classification_Project.MaxScaler import MaxScaler
from Classification_Project.MethodResultsArchiver import MethodResultsArchiver
from Classification_Project.Plotter import plotter
from Classification_Project.PolynomialFactory import PolynomialFactory, polynomial_factory


class ClassificationService:
    def __init__(self):
        self.classifier_factory = ClassifierFactory()
        self.polynomial_factory = PolynomialFactory()
        self.data_extractor = DataExtractor()
        self.scaler = MaxScaler()
        self.archiver = MethodResultsArchiver()
        self.method_reader = ClassificationMethodReader()

    def classify_and_get_info(self, classification_dto):
        try:
            classification_result = self.__classify(classification_dto)

            file_utils.numpy_save_session_based_txt_file(classification_result.train_prediction,
                                                         classification_dto.classifier_name + '_train_predictions.csv')
            file_utils.numpy_save_session_based_txt_file(classification_result.test_prediction,
                                                         classification_dto.classifier_name + '_test_predictions.csv')

            return self.__map_to_response_dto(classification_result)

        except Exception as e:
            console_logger.error(f'Classification failed. {str(e)}', e)
            raise BadRequest(str(e))

    def get_classification_result_archive(self, method_name):
        try:
            if not file_utils.is_classification_result_files_exists(method_name):
                console_logger.error('Can\'t get data. No calculations were performed.')
                raise Exception('Can\'t get data. No calculations were performed.')

            result = self.archiver.archive_method_results(method_name)

            return result

        except Exception as e:
            console_logger.error(f'Classification failed. {str(e)}')
            raise BadRequest(str(e))

    def get_available_methods(self):
        return json.dumps(classification_method_reader.read_all_available_methods())

    def compare_classification(self):
        methods_names = list(map(lambda m: m['name'], classification_method_reader.read_all_available_methods()))
        result = {}

        for method_name in methods_names:
            classifier = self.classifier_factory.get_default_args_classifier(method_name)

            result[method_name] = self.__classify_with_default_args(classifier)

            file_utils.numpy_save_session_based_txt_file(result[method_name].train_prediction,
                                                         method_name + '_train_predictions.csv')
            file_utils.numpy_save_session_based_txt_file(result[method_name].test_prediction,
                                                         method_name + '_test_predictions.csv')

        return result

    def build_fit_time_plot(self):
        return plotter.build_histogram(self.compare_classification(), 'fit_time')

    def build_test_accuracy_plot(self):
        return plotter.build_histogram(self.compare_classification(), 'test_accuracy', descending=True)

    def __classify(self, classification_dto):
        console_logger.info('Extracting train data')
        train_data = self.data_extractor.extract_data('train_data.txt')
        console_logger.info('Extracting test data')
        test_data = self.data_extractor.extract_data('test_data.txt')

        if classification_dto.is_polynomial_used:
            console_logger.info("Data transformation...")
            self.__fit(train_data, test_data)
            self.__polynomial_transformation(train_data, test_data, classification_dto.polynomial_name,
                                             classification_dto.polynomial_params_dictionary)
            console_logger.info('Data transformation finished')

        classifier = self.classifier_factory.get_classifier(classification_dto.classifier_name,
                                                            classification_dto.classifier_params_dictionary)

        console_logger.info('Classification started...')
        result = ClassifierEngine(classifier).classify(train_data, test_data)
        console_logger.info('Classification successfully finished...')

        return result

    def __classify_with_default_args(self, classifier):
        console_logger.info('Extracting train data')
        train_data = self.data_extractor.extract_data('train_data.txt')
        console_logger.info('Extracting test data')
        test_data = self.data_extractor.extract_data('test_data.txt')

        console_logger.info("Data transformation...")
        self.__fit(train_data, test_data)
        self.__default_polynomial_transformation(train_data, test_data)
        console_logger.info('Data transformation finished')

        console_logger.info('Classification started...')
        result = ClassifierEngine(classifier).classify(train_data, test_data)
        console_logger.info('Classification successfully finished...')

        return result

    def __fit(self, train_data, test_data):
        self.scaler.fit(train_data.x)

        train_data.x = self.scaler.transform(train_data.x)
        test_data.x = self.scaler.transform(test_data.x)

    def __polynomial_transformation(self, train_data, test_data, polynomial_name, polynomial_params):
        polynomial = self.polynomial_factory.get_polynomial(polynomial_name, polynomial_params)

        train_data.x = polynomial.fit_transform(train_data.x)
        test_data.x = polynomial.fit_transform(test_data.x)

    def __default_polynomial_transformation(self, train_data, test_data):
        polynomial = polynomial_factory.get_default_args_polynomial()

        train_data.x = polynomial.fit_transform(train_data.x)
        test_data.x = polynomial.fit_transform(test_data.x)

    def map_to_default_response_dto(self, classification_result):
        mapped_result = {}

        for method_name in classification_result.keys():
            mapped_result[method_name] = self.__map_to_response_dto(classification_result[method_name]).serialize

        return DefaultClassificationResponseDto(mapped_result)

    def __map_to_response_dto(self, classification_result):
        result = ClassificationResponseDto()

        result.test_prediction_time = classification_result.test_prediction_time
        result.train_prediction_time = classification_result.train_prediction_time
        result.fit_time = classification_result.fit_time
        result.test_accuracy = classification_result.test_accuracy
        result.train_accuracy = classification_result.train_accuracy

        return result
