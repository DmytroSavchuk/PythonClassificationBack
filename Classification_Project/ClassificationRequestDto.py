class ClassificationRequestDto:
    def __init__(self):
        self.polynomial_name = None
        self.polynomial_params_dictionary = None
        self.classifier_name = None
        self.classifier_params_dictionary = None
        self.is_polynomial_used = None

    @property
    def serialize(self):
        return {
            'polynomial_name': self.polynomial_name,
            'polynomial_params_dictionary': self.polynomial_params_dictionary,
            'classifier_name': self.classifier_name,
            'classifier_params_dictionary': self.classifier_params_dictionary,
            'is_polynomial_used': self.is_polynomial_used
        }
