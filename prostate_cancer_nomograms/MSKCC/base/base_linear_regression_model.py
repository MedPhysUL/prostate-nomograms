import pandas as pd
import numpy as np


class BaseLinearRegressionModel:

    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame
    ):
        super(BaseLinearRegressionModel, self).__init__()
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
        psa = np.array(self.patients_information["Diag_PSA"])
        knot1 = self.spline_knots_values["PSAPreopKnot1"]
        knot3 = self.spline_knots_values["PSAPreopKnot3"]
        knot4 = self.spline_knots_values["PSAPreopKnot4"]

        spline_term_1 = np.maximum(psa - knot1, np.zeros_like(psa))**3
        spline_term_1 += -(np.maximum(psa - knot3, np.zeros_like(psa))**3) * (knot4 - knot1) / (knot4 - knot3)
        spline_term_1 += (np.maximum(psa - knot4, np.zeros_like(psa))**3) * (knot3 - knot1) / (knot4 - knot3)

        return spline_term_1

    @property
    def spline_term_2(self) -> np.ndarray:
        psa = np.array(self.patients_dataframe["Diag_PSA"])
        knot2 = self.spline_knots_values["PSAPreopKnot2"]
        knot3 = self.spline_knots_values["PSAPreopKnot3"]
        knot4 = self.spline_knots_values["PSAPreopKnot4"]

        spline_term_2 = np.maximum(psa - knot2, np.zeros_like(psa)) ** 3
        spline_term_2 += -(np.maximum(psa - knot3, np.zeros_like(psa)) ** 3) * (knot4 - knot2) / (knot4 - knot3)
        spline_term_2 += (np.maximum(psa - knot4, np.zeros_like(psa)) ** 3) * (knot3 - knot2) / (knot4 - knot3)

        return spline_term_2

    @property
    def predicted_result(self):
        raise NotImplementedError()
