from typing import Union

import numpy as np
from sksurv.linear_model import CoxPHSurvivalAnalysis


class SurvivalRegression:

    def __init__(self):
        """
        Logistic regression.
        """
        self.classifier = CoxPHSurvivalAnalysis()

    def fit(self, capra_score: np.ndarray, event_indicator: np.ndarray, event_time: np.ndarray):
        """
        Fits the model.

        Parameters
        ----------
        capra_score : numpy.ndarray
            The CAPRA score.
        event_indicator : numpy.ndarray
            The event indicator.
        event_time : numpy.ndarray
            The event time.
        """
        self.classifier.fit(X=capra_score, y=np.concatenate(event_indicator, event_time))

    def get_predicted_survival_probability(
            self,
            capra_score: np.ndarray,
            number_of_years: Union[np.ndarray, list, float, int]
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        capra_score : numpy.ndarray
            The CAPRA score.
        number_of_years : Union[numpy.ndarray, list, float, int]
            The number of years.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        survival_func = self.classifier.predict_survival_function(X=np.array(capra_score).reshape(-1, 1))
        return survival_func(number_of_years)
