from werkzeug.exceptions import BadRequest

from Classification_Project.ClassificationRequestDto import ClassificationRequestDto
from Classification_Project.ConsoleLogger import console_logger


class ClassificationRequestDtoMapper:
    def map(self, dictionary):
        result = ClassificationRequestDto()

        try:
            result.is_polynomial_used = dictionary['is_polynomial_used']
            result.classifier_params_dictionary = dictionary['classifier_params_dictionary']
            result.classifier_name = dictionary['classifier_name']

            if result.is_polynomial_used:
                result.polynomial_params_dictionary = dictionary['polynomial_params_dictionary']
                result.polynomial_name = dictionary['polynomial_name']
        except Exception:
            console_logger.error('Can\'t map parameters. Some parameters are missed or are invalid.')
            raise BadRequest('Can\'t map parameters. Some parameters are missed or are invalid.')

        return result


classification_request_mapper = ClassificationRequestDtoMapper()
