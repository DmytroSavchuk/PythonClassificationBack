from collections import namedtuple

from flask import session
from werkzeug.exceptions import BadRequest

from classification_project.Archiver import Archiver
from classification_project.ClassificationResponseDto import ClassificationResponseDto
from classification_project.ClassifierEngine import ClassifierEngine
from classification_project.ClassifierFactory import ClassifierFactory
from classification_project.DataExtractor import DataExtractor
from classification_project.MaxScaler import MaxScaler
from classification_project.PolynomialFactory import PolynomialFactory


class ClassificationService:
    def __init__(self):
        self.classifier_factory = ClassifierFactory()
        self.polynomial_factory = PolynomialFactory()
        self.data_extractor = DataExtractor()
        self.scaler = MaxScaler()
        self.archiver = Archiver()

    def classify_and_get_info(self, classification_dto):
        try:
            classification_result = self.__classify(classification_dto)

            session['last_classify_and_get_info_request'] = classification_dto.serialize

            return self.__map_to_response_dto(classification_result)

        except Exception as e:
            raise BadRequest(str(e))

    def classify_and_get_data(self):
        try:
            if session.get('last_classify_and_get_info_request') is None:
                raise Exception('Can\'t get data. No calculations were performed.')

            classification_result = self.__classify(
                namedtuple('ClassificationRequestDto', session['last_classify_and_get_info_request'].keys())
                (*session['last_classify_and_get_info_request'].values()))

            return self.archiver.archive(classification_result.train_prediction, classification_result.test_prediction)

        except Exception as e:
            raise BadRequest(str(e))

    def __classify(self, classification_dto):
        train_data = self.data_extractor.extract_data('train_data')
        test_data = self.data_extractor.extract_data('test_data')

        self.__fit(train_data, test_data)
        self.__polynomial_transformation(train_data, test_data, classification_dto.polynomial_name,
                                         classification_dto.polynomial_params_dictionary)

        classifier = self.classifier_factory.get_classifier(classification_dto.classifier_name,
                                                            classification_dto.classifier_params_dictionary)

        return ClassifierEngine(classifier).classify(train_data, test_data)

    def __fit(self, train_data, test_data):
        self.scaler.fit(train_data.x)

        train_data.x = self.scaler.transform(train_data.x)
        test_data.x = self.scaler.transform(test_data.x)

    def __polynomial_transformation(self, train_data, test_data, polynomial_name, polynomial_params):
        polynomial = self.polynomial_factory.get_polynomial(polynomial_name, polynomial_params)

        train_data.x = polynomial.fit_transform(train_data.x)
        test_data.x = polynomial.fit_transform(test_data.x)

    def __map_to_response_dto(self, classification_result):
        result = ClassificationResponseDto()

        result.test_prediction_time = classification_result.test_prediction_time
        result.train_prediction_time = classification_result.train_prediction_time
        result.fit_time = classification_result.fit_time
        result.test_accuracy = classification_result.test_accuracy
        result.train_accuracy = classification_result.train_accuracy

        return result
