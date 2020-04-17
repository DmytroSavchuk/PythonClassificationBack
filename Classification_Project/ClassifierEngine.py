import time

from sklearn.metrics import accuracy_score

from classification_project.ClassificationResult import ClassificationResult


class ClassifierEngine:
    def __init__(self, classifier):
        self.classifier = classifier

    def classify(self, train_data, test_data):
        result = ClassificationResult()

        self.__fit(train_data, result)
        self.__predict(train_data, test_data, result)
        self.__calculate_accuracy(train_data, test_data, result)

        return result

    def __fit(self, train_data, classification_result):
        start_time = time.time()

        self.classifier.fit(train_data.x, train_data.y)

        classification_result.fit_time = time.time() - start_time

    def __predict(self, train_data, test_data, classification_result):
        start_time = time.time()

        classification_result.train_prediction = self.classifier.predict(train_data.x)
        classification_result.train_prediction_time = time.time() - start_time

        start_time = time.time()

        classification_result.test_prediction = self.classifier.predict(test_data.x)
        classification_result.test_prediction_time = time.time() - start_time

    def __calculate_accuracy(self, train_data, test_data, classification_result):
        classification_result.train_accuracy = accuracy_score(train_data.y, classification_result.train_prediction)
        classification_result.test_accuracy = accuracy_score(test_data.y, classification_result.test_prediction)
