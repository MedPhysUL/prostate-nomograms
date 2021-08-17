from typing import Union

import pandas as pd
import numpy as np
from .logistic_regression_model import LogisticRegressionModel


class SurvivalRegressionModel(LogisticRegressionModel):
    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame,
            model_name: str
    ):
        super(SurvivalRegressionModel, self).__init__(
            patients_dataframe=patients_dataframe,
            variables_dataframe=variables_dataframe,
            spline_knots_dataframe=spline_knots_dataframe,
            model_name=model_name
        )

    def get_predicted_survival_probability(self, number_of_years: Union[float, int]):
        predicted_result = self.predicted_result
        scaling_parameter = self.variables_values["Scaling Parameter"]

        num = 1 + (np.exp(-predicted_result) * 0) ** (1 / scaling_parameter)
        denum = 1 + (np.exp(-predicted_result) * number_of_years) ** (1 / scaling_parameter)

        return num/denum
