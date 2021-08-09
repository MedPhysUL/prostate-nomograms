from abc import ABC

import pandas as pd
import numpy as np
from .base_linear_regression_model import BaseLinearRegressionModel


class BaseLogisticRegressionModel(BaseLinearRegressionModel, ABC):
    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame
    ):
        super(BaseLogisticRegressionModel, self).__init__(
            patients_dataframe=patients_dataframe,
            variables_dataframe=variables_dataframe,
            spline_knots_dataframe=spline_knots_dataframe
        )

    def get_predicted_probability(self):
        predicted_result = self.predicted_result
        return np.exp(predicted_result)/(1 + np.exp(predicted_result))
