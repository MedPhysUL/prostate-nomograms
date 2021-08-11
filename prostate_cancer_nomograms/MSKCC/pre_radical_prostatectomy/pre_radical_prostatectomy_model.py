import os
from typing import Union
from .models.logistic_regression_model import LogisticRegressionModel
from .models.survival_regression_model import SurvivalRegressionModel
from .model_name import ModelName
from prostate_cancer_nomograms.utils import *
from prostate_cancer_nomograms.MSKCC.base.base_model import BaseModel
import pandas as pd
import numpy as np


class PreRadicalProstatectomyModel(BaseModel):

    def __init__(self, patients_dataframe: pd.DataFrame, model_name: str):
        if model_name in ModelName.list():
            pass
        else:
            raise ValueError(f"Given model name {model_name} is not allowed. Allowed values are {ModelName.list()}"
                             f".")

        super(PreRadicalProstatectomyModel, self).__init__(
            patients_dataframe=patients_dataframe,
            model_name=model_name
        )

    @property
    def url(self):
        return "https://www.mskcc.org/nomograms/prostate/pre_op/coefficients"

    @property
    def json_folder_path(self):
        return os.path.join(os.path.dirname(__file__), "models_coefficients")

    def get_predictions(self, number_of_years: Union[np.ndarray, list, float, int] = None):
        if self.model_type == "survival":
            if number_of_years is None:
                raise ValueError("Number of years must be given.")
            else:
                survival_regression_model = SurvivalRegressionModel(
                    patients_dataframe=self.patients_dataframe,
                    variables_dataframe=self.variables_dataframe,
                    spline_knots_dataframe=self.spline_dataframe,
                    model_name=self.model_name
                )

                return survival_regression_model.get_predicted_survival_probability(number_of_years=number_of_years)

        elif self.model_type == "logistic":
            logistic_regression_model = LogisticRegressionModel(
                patients_dataframe=self.patients_dataframe,
                variables_dataframe=self.variables_dataframe,
                spline_knots_dataframe=self.spline_dataframe,
                model_name=self.model_name
            )

            return logistic_regression_model.get_predicted_probability()

        else:
            raise ValueError(f"Model type {self.model_type} doesn't exist.")


