import pandas as pd
import numpy as np


class LinearRegressionModel:

    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame
    ):
        super(LinearRegressionModel, self).__init__()
        self.patients_dataframe = patients_dataframe
        self.variables_dataframe = variables_dataframe
        self.spline_knots_dataframe = spline_knots_dataframe

    @property
    def patients_information(self):
        return self.patients_dataframe.to_dict(orient="list")

    @staticmethod
    def get_dict_from_two_columns_of_a_dataframe(
            dataframe: pd.DataFrame,
            keys_column_name: str,
            values_column_name: str
    ):
        return pd.Series(data=dataframe[values_column_name].values, index=dataframe[keys_column_name]).to_dict()

    @property
    def variables_values(self) -> dict:
        variables_values = self.get_dict_from_two_columns_of_a_dataframe(
            dataframe=self.variables_dataframe,
            keys_column_name="Variable",
            values_column_name="Value"
        )

        return variables_values

    @property
    def spline_knots_values(self) -> dict:
        spline_knots_values = self.get_dict_from_two_columns_of_a_dataframe(
            dataframe=self.spline_knots_dataframe,
            keys_column_name="Knot",
            values_column_name="Value"
        )

        return spline_knots_values

    @property
    def spline_term_1(self) -> np.ndarray:
        psa = np.array(self.patients_information["PSA"])
        knot1 = self.spline_knots_values["PSAPreopKnot1"]
        knot3 = self.spline_knots_values["PSAPreopKnot3"]
        knot4 = self.spline_knots_values["PSAPreopKnot4"]

        spline_term_1 = np.maximum(psa - knot1, np.zeros_like(psa))**3
        spline_term_1 += -(np.maximum(psa - knot3, np.zeros_like(psa))**3) * (knot4 - knot1) / (knot4 - knot3)
        spline_term_1 += (np.maximum(psa - knot4, np.zeros_like(psa))**3) * (knot3 - knot1) / (knot4 - knot3)

        return spline_term_1

    @property
    def spline_term_2(self) -> np.ndarray:
        psa = np.array(self.patients_dataframe["PSA"])
        knot2 = self.spline_knots_values["PSAPreopKnot2"]
        knot3 = self.spline_knots_values["PSAPreopKnot3"]
        knot4 = self.spline_knots_values["PSAPreopKnot4"]

        spline_term_2 = np.maximum(psa - knot2, np.zeros_like(psa)) ** 3
        spline_term_2 += -(np.maximum(psa - knot3, np.zeros_like(psa)) ** 3) * (knot4 - knot2) / (knot4 - knot3)
        spline_term_2 += (np.maximum(psa - knot4, np.zeros_like(psa)) ** 3) * (knot3 - knot2) / (knot4 - knot3)

        return spline_term_2

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
