from __future__ import annotations
from typing import Optional, Union

import pandas as pd
import numpy as np

from .logistic_regression import LogisticRegression


class SurvivalRegression(LogisticRegression):

    def get_predicted_risk(
            self,
            dataframe: pd.DataFrame,
            regressor_as_variable: Optional[SurvivalRegression] = None,
    ) -> np.array:
        """
        Gets the predicted risk. The predicted risk is the predicted probability multiplied by the scaling parameter.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe that contains the patients data.
        regressor_as_variable : Optional[SurvivalRegression]
            The regressor as variable.

        Returns
        -------
        predicted_risk : numpy.ndarray
            The predicted risk.
        """
        if regressor_as_variable:
            predicted_result = self.get_predicted_result(dataframe, regressor_as_variable)
        else:
            predicted_result = self.get_predicted_result(dataframe)

        scaling_parameter = self.variables_coefficients["Scaling Parameter"]

        return -predicted_result/scaling_parameter

    def get_predicted_survival_probability(
            self,
            dataframe: pd.DataFrame,
            number_of_months: Union[np.ndarray, list, float, int],
            regressor_as_variable: Optional[SurvivalRegression] = None,
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe that contains the patients data.
        number_of_months : Union[numpy.ndarray, list, float, int]
            The number of years.
        regressor_as_variable : Optional[SurvivalRegression]
            The regressor as variable.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        if regressor_as_variable:
            predicted_result = self.get_predicted_result(dataframe, regressor_as_variable)
        else:
            predicted_result = self.get_predicted_result(dataframe)

        scaling_parameter = self.variables_coefficients["Scaling Parameter"]

        num = 1 + (np.exp(-predicted_result) * 0) ** (1 / scaling_parameter)
        denum = 1 + (np.exp(-predicted_result) * number_of_months/12) ** (1 / scaling_parameter)

        return num/denum
