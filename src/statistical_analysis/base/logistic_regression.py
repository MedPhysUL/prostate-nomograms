from typing import Union
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd


class CustomLogisticRegression:

    def __init__(self, x: pd.DataFrame, y: pd.DataFrame, positive_label: Union[str, int]):
        self.x = x
        self.y = y
        self.positive_label = positive_label

    @property
    def score_array(self):
        return np.array(self.x).reshape(-1, 1)

    @property
    def binary_outcome_array(self):
        binary_outcome = pd.DataFrame(data=np.zeros(len(self.y.index)), index=self.y.index)
        positive_value_idx = self.y.index[self.y == self.positive_label].tolist()
        binary_outcome.loc[positive_value_idx] = 1
        binary_outcome_array = np.array(binary_outcome).ravel()

        return binary_outcome_array

    @property
    def classifier(self):
        clf = LogisticRegression().fit(
            X=self.score_array,
            y=self.binary_outcome_array
        )

        return clf

    @property
    def predicted_probability(self):
        return self.classifier.predict_proba(X=self.score_array)[:, 1]
