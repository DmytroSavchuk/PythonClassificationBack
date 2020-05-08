import copy

from sklearn.preprocessing import PolynomialFeatures

from Classification_Project.IllegalArgumentException import IllegalArgumentException

DEFAULT_POLYNOMIAL_DEGREE = 2


class PolynomialFactory:
    def __init__(self):
        self.polynomial_prototypes = []

        self.polynomial_prototypes.append(PolynomialFeatures())

    def get_polynomial(self, polynomial_class_name, params_dictionary):
        polynomial = copy.deepcopy(self.__find_prototype(polynomial_class_name))

        self.__fill_polynomial_params(polynomial, params_dictionary)

        return polynomial

    def get_default_args_polynomial(self):
        return PolynomialFeatures(degree=DEFAULT_POLYNOMIAL_DEGREE)

    def __fill_polynomial_params(self, polynomial, params_dictionary):
        for param in params_dictionary:
            if not hasattr(polynomial, param):
                raise IllegalArgumentException('%s doesn\'t contain %s parameter.' % type(polynomial).__name__,
                                               param)

            setattr(polynomial, param, params_dictionary[param])

    def __find_prototype(self, polynomial_class_name):
        for proto in self.polynomial_prototypes:
            if type(proto).__name__.lower() == polynomial_class_name.lower():
                return proto

        raise IllegalArgumentException('Given polynomial name is incorrect. There is no polynomial with name %s.' %
                                       polynomial_class_name)


polynomial_factory = PolynomialFactory()
