from typing import Union

import pandas as pd
import numpy as np
from prostate_cancer_nomograms.MSKCC.base.base_surivival_regression_model import BaseSurvivalRegressionModel


class SurvivalRegressionModel(BaseSurvivalRegressionModel):
    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame
    ):
        super(SurvivalRegressionModel, self).__init__(
            patients_dataframe=patients_dataframe,
            variables_dataframe=variables_dataframe,
            spline_knots_dataframe=spline_knots_dataframe
        )

    @property
    def gleason_value(self) -> np.ndarray:
        primary_gleason = np.array(self.patients_dataframe["Primary Gleason"])
        secondary_gleason = np.array(self.patients_dataframe["Secondary Gleason"])
        total_gleason_score = primary_gleason + secondary_gleason

        gleason_value = np.zeros_like(total_gleason_score, dtype=float)

        gleason_value[total_gleason_score == 6] = self.variables_values["Pathologic Gleason Grade Group 2"]
        gleason_value[total_gleason_score == 7] = self.variables_values["Pathologic Gleason Grade Group 3"]
        gleason_value[total_gleason_score == 8] = self.variables_values["Pathologic Gleason Grade Group 4"]
        gleason_value[total_gleason_score == 9] = self.variables_values["Pathologic Gleason Grade Group 5"]
        gleason_value[total_gleason_score == 10] = self.variables_values["Pathologic Gleason Grade Group 5"]

        return gleason_value

    @property
    def predicted_result(self):
        result = self.variables_values["Intercept"]
        result += np.array(self.patients_information["PSA"]) * self.variables_values["Preoperative PSA"]
        result += self.spline_term_1 * self.variables_values["Preoperative PSA Spline 1"]
        result += self.spline_term_2 * self.variables_values["Preoperative PSA Spline 2"]
        result += np.array(self.patients_information["Age"]) * self.variables_values["Patient Age"]
        result += self.gleason_value

        surgical_margins = self.patients_information["Surgical Margin Status"]
        extra_capsular = self.patients_information["Extracapsular Extension"]
        seminal_vesicles = self.patients_information["Seminal Vesicle Invasion"]
        pelvic_lymph_nodes = self.patients_information["Lymph Node Involvement"]

        result[surgical_margins] += self.variables_values["Surgical Margin Status"]
        result[extra_capsular] += self.variables_values["Extracapsular Extension"]
        result[seminal_vesicles] += self.variables_values["Seminal Vesicle Invasion"]
        result[pelvic_lymph_nodes] += self.variables_values["Lymph Node Involvement"]

        return result

    def get_predicted_survival_probability(self, number_of_years: Union[np.ndarray, list, float, int]):
        predicted_result = self.predicted_result
        scaling_parameter = self.variables_values["Scaling Parameter"]

        num = 1 + (np.exp(-predicted_result) * self.patients_information["Free Months"]/12) ** (1 / scaling_parameter)
        denum = 1 + (np.exp(-predicted_result) * np.array(number_of_years)) ** (1 / scaling_parameter)

        return num/denum
