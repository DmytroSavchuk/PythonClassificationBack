from classification_project.ClassificationRequestDto import ClassificationRequestDto


class ClassificationRequestDtoMapper:
    def map(self, dictionary):
        result = ClassificationRequestDto()

        result.polynomial_params_dictionary = dictionary['polynomial_params_dictionary']
        result.classifier_params_dictionary = dictionary['classifier_params_dictionary']
        result.classifier_name = dictionary['classifier_name']
        result.polynomial_name = dictionary['polynomial_name']

        return result
