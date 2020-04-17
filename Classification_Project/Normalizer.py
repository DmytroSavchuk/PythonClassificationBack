class Normalizer:
    def __init__(self, scaler):
        self.scaler = scaler

    def normalize(self, scaler, data, do_fit):
        if do_fit:
            scaler.fit(data)

        return scaler.transform(data)
