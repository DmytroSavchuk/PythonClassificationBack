import copy

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from classification_project.IllegalArgumentException import IllegalArgumentException


class ClassifierFactory:
    def __init__(self):
        self.classifier_prototypes = []

        self.classifier_prototypes.append(DecisionTreeClassifier())
        self.classifier_prototypes.append(RandomForestClassifier())
        self.classifier_prototypes.append(ExtraTreesClassifier())
        self.classifier_prototypes.append(LogisticRegression())
        self.classifier_prototypes.append(MLPClassifier())
        self.classifier_prototypes.append(LinearSVC())
        self.classifier_prototypes.append(SVC())

    def get_classifier(self, classifier_class_name, params_dictionary):
        classifier = copy.deepcopy(self.__find_prototype(classifier_class_name))

        self.__fill_classifier_params(classifier, params_dictionary)

        return classifier

    def __fill_classifier_params(self, classifier, params_dictionary):
        for param in params_dictionary:
            if not hasattr(classifier, param):
                raise IllegalArgumentException('%s doesn\'t contain %s parameter.' % type(classifier).__name__,
                                               param)

            setattr(classifier, param, params_dictionary[param])

    def __find_prototype(self, classifier_class_name):
        for proto in self.classifier_prototypes:
            if type(proto).__name__.lower() == classifier_class_name.lower():
                return proto

        raise IllegalArgumentException('Given classifier name is incorrect. There is no classifier with name %s.' %
                                       classifier_class_name)

