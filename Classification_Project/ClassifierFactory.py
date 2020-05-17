import copy

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from Classification_Project.ClassificationMethodReader import classification_method_reader
from Classification_Project.ConsoleLogger import console_logger
from Classification_Project.IllegalArgumentException import IllegalArgumentException


class ClassifierFactory:
    def __init__(self):
        self.classifier_prototypes = []
        self.methods_params = classification_method_reader.read_all_available_methods()

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

        console_logger.info(f'Using {classifier_class_name} with parameters: {params_dictionary}')

        return classifier

    def get_default_args_classifier(self, classifier_class_name):
        method_params = list(filter(lambda m: m['name'] == classifier_class_name, self.methods_params))[0]
        default_args = self.__extract_default_args(method_params)

        classifier = copy.deepcopy(self.__find_prototype(classifier_class_name))

        self.__fill_classifier_params(classifier, default_args)

        return classifier

    def get_available_classifier_names(self):
        return list(map(lambda m: m['name'], self.methods_params))

    def __extract_default_args(self, method_params):
        default_args = {}

        for arg in method_params['methodArgs'].keys():
            default_args[arg] = method_params['methodArgs'][arg]['defaultValue']

        return default_args

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


classifier_factory = ClassifierFactory()
