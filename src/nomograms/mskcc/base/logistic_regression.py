from __future__ import annotations
from typing import Mapping, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .survival_regression import SurvivalRegression

import numpy as np
import pandas as pd


class LogisticRegression:

    def __init__(
            self,
            variables_coefficients: Mapping[str, float],
            spline_coefficients: Mapping[str, float],
            cores: bool,
            age_column_name: str = "AGE",
            psa_column_name: str = "PSA",
            primary_gleason_column_name: str = "GLEASON_PRIMARY",
            secondary_gleason_column_name: str = "GLEASON_SECONDARY",
            clinical_stage_column_name: str = "CLINICAL_STAGE",
            number_of_positive_cores_column_name: Optional[str] = None,
            number_of_negative_cores_column_name: Optional[str] = None,
    ):
        """
        Initializes columns names.

        Parameters
        ----------
        variables_coefficients : Mapping[str, float]
            Coefficients of the variables.
        spline_coefficients : Mapping[str, float]
            Coefficients of the splines.
        cores : bool
            Whether to use the number of positive and negative cores.
        age_column_name : str
            Name of the column containing the age of the patients.
        psa_column_name : str
            Name of the column containing the PSA of the patients.
        primary_gleason_column_name : str
            Name of the column containing the primary Gleason score of the patients.
        secondary_gleason_column_name : str
            Name of the column containing the secondary Gleason score of the patients.
        clinical_stage_column_name : str
            Name of the column containing the clinical stage of the patients.
        number_of_positive_cores_column_name : str, optional
            Name of the column containing the number of positive cores of the patients.
        number_of_negative_cores_column_name : str, optional
            Name of the column containing the number of negative cores of the patients.
        """
        self.variables_coefficients = variables_coefficients
        self.spline_coefficients = spline_coefficients
        self.cores = cores

        self.age_column_name = age_column_name
        self.psa_column_name = psa_column_name
        self.primary_gleason_column_name = primary_gleason_column_name
        self.secondary_gleason_column_name = secondary_gleason_column_name
        self.clinical_stage_column_name = clinical_stage_column_name
        self.number_of_positive_cores = number_of_positive_cores_column_name
        self.number_of_negative_cores = number_of_negative_cores_column_name

    def _get_gleason_value(self, data_dict: dict) -> np.ndarray:
        primary_gleason = np.array(data_dict[self.primary_gleason_column_name])
        secondary_gleason = np.array(data_dict[self.secondary_gleason_column_name])
        total_gleason_score = primary_gleason + secondary_gleason

        gleason_value = np.zeros_like(total_gleason_score, dtype=float)
        mask_grade_2 = np.where(((primary_gleason == 3) & (secondary_gleason == 4)), True, False)
        mask_grade_3 = np.where(((primary_gleason == 4) & (secondary_gleason == 3)), True, False)

        gleason_value[mask_grade_2] = self.variables_coefficients["Biopsy Gleason Grade Group 2"]
        gleason_value[mask_grade_3] = self.variables_coefficients["Biopsy Gleason Grade Group 3"]
        gleason_value[total_gleason_score == 8] = self.variables_coefficients["Biopsy Gleason Grade Group 4"]
        gleason_value[total_gleason_score == 9] = self.variables_coefficients["Biopsy Gleason Grade Group 5"]
        gleason_value[total_gleason_score == 10] = self.variables_coefficients["Biopsy Gleason Grade Group 5"]

        return gleason_value

    def _get_clinical_stage_value(self, data_dict: dict) -> np.ndarray:
        tumor_stage = data_dict[self.clinical_stage_column_name]

        clinical_stage_value = np.zeros_like(tumor_stage, dtype=float)
        clinical_stage_value[list(map("T2a".__eq__, tumor_stage))] = self.variables_coefficients["Clinical Stage 2A"]
        clinical_stage_value[list(map("T2b".__eq__, tumor_stage))] = self.variables_coefficients["Clinical Stage 2B"]
        clinical_stage_value[list(map("T2c".__eq__, tumor_stage))] = self.variables_coefficients["Clinical Stage 2C"]
        clinical_stage_value[list(map("T3a".__eq__, tumor_stage))] = self.variables_coefficients["Clinical Stage 3+"]
        clinical_stage_value[list(map("T3b".__eq__, tumor_stage))] = self.variables_coefficients["Clinical Stage 3+"]
        clinical_stage_value[list(map("T3c".__eq__, tumor_stage))] = self.variables_coefficients["Clinical Stage 3+"]

        return clinical_stage_value

    def _get_positive_cores_value(self, data_dict: dict) -> np.ndarray:
        return np.array(data_dict[self.number_of_positive_cores])*self.variables_coefficients["No. of Positive Cores"]

    def _get_negative_cores_value(self, data_dict: dict):
        return np.array(data_dict[self.number_of_negative_cores])*self.variables_coefficients["No. of Negative Cores"]

    def _get_spline_term_1(self, psa: np.array) -> np.ndarray:
        """
        Gets the spline term 1.

        Parameters
        ----------
        psa : numpy.ndarray
            The PSA values.

        Returns
        -------
        spline_term_1 : numpy.ndarray
            The spline term 1.
        """
        knot1 = self.spline_coefficients["PSAPreopKnot1"]
        knot3 = self.spline_coefficients["PSAPreopKnot3"]
        knot4 = self.spline_coefficients["PSAPreopKnot4"]

        spline_term_1 = np.maximum(psa - knot1, np.zeros_like(psa))**3
        spline_term_1 += -(np.maximum(psa - knot3, np.zeros_like(psa))**3) * (knot4 - knot1) / (knot4 - knot3)
        spline_term_1 += (np.maximum(psa - knot4, np.zeros_like(psa))**3) * (knot3 - knot1) / (knot4 - knot3)

        return spline_term_1

    def _get_spline_term_2(self, psa: np.array) -> np.ndarray:
        """
        Gets the spline term 2.

        Parameters
        ----------
        psa : numpy.ndarray
            The PSA values.

        Returns
        -------
        spline_term_2 : numpy.ndarray
            The spline term 2.
        """
        knot2 = self.spline_coefficients["PSAPreopKnot2"]
        knot3 = self.spline_coefficients["PSAPreopKnot3"]
        knot4 = self.spline_coefficients["PSAPreopKnot4"]

        spline_term_2 = np.maximum(psa - knot2, np.zeros_like(psa)) ** 3
        spline_term_2 += -(np.maximum(psa - knot3, np.zeros_like(psa)) ** 3) * (knot4 - knot2) / (knot4 - knot3)
        spline_term_2 += (np.maximum(psa - knot4, np.zeros_like(psa)) ** 3) * (knot3 - knot2) / (knot4 - knot3)

        return spline_term_2

    def get_predicted_result(
            self,
            dataframe: pd.DataFrame,
            regressor_as_variable: Optional[SurvivalRegression] = None
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe that contains the patients data.
        regressor_as_variable : Optional[SurvivalRegression]
            The regressor as variable.

        Returns
        -------
        predicted_result : numpy.ndarray
            The predicted result.
        """
        data_dict = dataframe.to_dict(orient="list")

        result = self.variables_coefficients["Intercept"]

        if regressor_as_variable:
            keys = [k for k in self.variables_coefficients.keys() if k.startswith("Survival probability")]
            assert len(keys) == 1, "There should be only one key that starts with 'Survival probability'"
            coefficient = self.variables_coefficients[keys[0]]
            result += coefficient*regressor_as_variable.get_predicted_survival_probability(dataframe, 60)
            return result
        else:
            result += np.array(data_dict[self.psa_column_name]) * self.variables_coefficients["Preoperative PSA"]

            spline_term_1 = self._get_spline_term_1(np.array(data_dict[self.psa_column_name]))
            spline_term_2 = self._get_spline_term_2(np.array(data_dict[self.psa_column_name]))
            result += spline_term_1 * self.variables_coefficients["Preoperative PSA Spline 1"]
            result += spline_term_2 * self.variables_coefficients["Preoperative PSA Spline 2"]

            result += np.array(data_dict[self.age_column_name]) * self.variables_coefficients["Patient Age"]
            result += self._get_gleason_value(data_dict)
            result += self._get_clinical_stage_value(data_dict)

            if self.cores:
                result += self._get_positive_cores_value(data_dict)
                result += self._get_negative_cores_value(data_dict)
            return result

    def get_predicted_probability(
            self,
            dataframe: pd.DataFrame,
            regressor_as_variable: Optional[SurvivalRegression] = None
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe that contains the patients data.
        regressor_as_variable : SurvivalRegression
            The regressor as variable.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        predicted_result = self.get_predicted_result(dataframe, regressor_as_variable)
        return np.exp(predicted_result)/(1 + np.exp(predicted_result))
