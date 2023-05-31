from typing import Union

import numpy as np
from sksurv.linear_model import CoxPHSurvivalAnalysis


class SurvivalRegression:

    def __init__(self, **kwargs):
        """
        Logistic regression.
        """
        self.classifier = CoxPHSurvivalAnalysis()

    def fit(
            self,
            capra_score: np.ndarray,
            event_indicator: np.ndarray,
            event_time: np.ndarray
    ):
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
        array = np.core.records.fromarrays((event_indicator, event_time), names="bool, float")
        self.classifier.fit(X=capra_score.reshape(-1, 1), y=array)

    def get_predicted_risk(
            self,
            capra_score: np.ndarray
    ) -> np.array:
        """
        Gets the predicted risk.

        Parameters
        ----------
        capra_score : numpy.ndarray
            The CAPRA score.

        Returns
        -------
        predicted_risk : numpy.ndarray
            The predicted risk.
        """
        return self.classifier.predict(X=capra_score.reshape(-1, 1))

    def get_predicted_survival_probability(
            self,
            capra_score: np.ndarray,
            number_of_months: Union[np.ndarray, list, float, int]
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        capra_score : numpy.ndarray
            The CAPRA score.
        number_of_months : Union[numpy.ndarray, list, float, int]
            The number of months.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        survival_funcs = self.classifier.predict_survival_function(X=capra_score.reshape(-1, 1))
        predicted_probability = []
        for survival_func in survival_funcs:
            predicted_probability.append(survival_func(number_of_months))

        return np.array(predicted_probability)
