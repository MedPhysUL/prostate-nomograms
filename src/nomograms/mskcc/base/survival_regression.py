from typing import Union

import pandas as pd
import numpy as np

from .logistic_regression import LogisticRegression


class SurvivalRegression(LogisticRegression):

    def get_predicted_survival_probability(
            self,
            dataframe: pd.DataFrame,
            number_of_years: Union[np.ndarray, list, float, int]
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe that contains the patients data.
        number_of_years : Union[numpy.ndarray, list, float, int]
            The number of years.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        predicted_result = self.get_predicted_result(dataframe)
        scaling_parameter = self.variables_coefficients["Scaling Parameter"]

        num = 1 + (np.exp(-predicted_result) * 0) ** (1 / scaling_parameter)
        denum = 1 + (np.exp(-predicted_result) * number_of_years) ** (1 / scaling_parameter)

        return num/denum
