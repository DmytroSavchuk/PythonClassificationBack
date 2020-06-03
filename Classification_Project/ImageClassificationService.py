from Classification_Project.ConsoleLogger import console_logger
from Classification_Project.Controller import file_utils
from Classification_Project.DataExtractor import DataExtractor


class ImageClassificationService:
    def __init__(self):
        # self.classifier_factory = ClassifierFactory()
        # self.polynomial_factory = PolynomialFactory()
        self.data_extractor = DataExtractor()
        # self.scaler = MaxScaler()
        # self.archiver = MethodResultsArchiver()
        # self.method_reader = ClassificationMethodReader()

    def classify_and_get_info(self, classification_dto):
        self.__classify()

    def __classify(self, classification_dto):
        console_logger.info('Extracting train data')
        train_data = file_utils.get_session_based_object('train_data')
        console_logger.info('Extracting test data')
        test_data = file_utils.get_session_based_object('test_data')

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
