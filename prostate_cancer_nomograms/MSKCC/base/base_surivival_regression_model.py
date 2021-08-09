from abc import ABC
from typing import Union

import pandas as pd
import numpy as np
from .base_linear_regression_model import BaseLinearRegressionModel


class BaseSurvivalRegressionModel(BaseLinearRegressionModel, ABC):
    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame
    ):
        super(BaseSurvivalRegressionModel, self).__init__(
            patients_dataframe=patients_dataframe,
            variables_dataframe=variables_dataframe,
            spline_knots_dataframe=spline_knots_dataframe
        )

    def get_predicted_survival_probability(self, number_of_years: Union[np.ndarray, list, float, int]):
        raise NotImplementedError()
