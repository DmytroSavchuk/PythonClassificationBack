from sklearn.base import BaseEstimator, ClassifierMixin
import numpy as np


class MaxScaler(BaseEstimator, ClassifierMixin):

    def __init__(self, name="MaxScaler"):
        self.name = name
        self.max_elements = None

    def fit(self, x):
        self.max_elements = np.amax(x, axis=0)
       
        return self

    def transform(self, x):
        return x / self.max_elements
