class ClassificationResponseDto:
    def __init__(self):
        self.fit_time = None
        self.train_prediction_time = None
        self.test_prediction_time = None
        self.train_accuracy = None
        self.test_accuracy = None

    @property
    def serialize(self):
        return {
            'fit_time': self.fit_time,
            'train_prediction_time': self.train_prediction_time,
            'test_prediction_time': self.test_prediction_time,
            'train_accuracy': self.train_accuracy,
            'test_accuracy': self.test_accuracy
        }
