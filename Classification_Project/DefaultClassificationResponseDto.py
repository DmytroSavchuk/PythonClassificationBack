class DefaultClassificationResponseDto:
    def __init__(self, result):
        self.result = result

    @property
    def serialize(self):
        return {
            'result': self.result
        }
