from typing import Mapping, Optional, Union

import numpy as np
import pandas as pd

from .logistic_regression import LogisticRegression
from .survival_regression import SurvivalRegression
from .web_table_scraper import CoefficientCategory, WebTableScraper


class Model:

    def __init__(
            self,
            outcome: str,
            url: str,
            json_folder_path: str,
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
        outcome : str
            Name of the outcome.
        url : str
            URL of the web page containing the coefficients.
        json_folder_path : str
            Path to save the coefficients.
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
        self.outcome = outcome

        web_table_scrapper = WebTableScraper(url, json_folder_path)
        coefficients_dataframe = web_table_scrapper.get_models_coefficients(CoefficientCategory.VARIABLES)
        self._variables_coefficients_dataframe = coefficients_dataframe[coefficients_dataframe["Model"] == outcome]
        self._splines_coefficients_dataframe = web_table_scrapper.get_models_coefficients(CoefficientCategory.SPLINE)

        if self.model_type == "survival":
            regressor_constructor = SurvivalRegression
        elif self.model_type == "logistic":
            regressor_constructor = LogisticRegression
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        self.regressor = regressor_constructor(
            variables_coefficients=self.variables_coefficients,
            spline_coefficients=self.spline_coefficients,
            cores=self.cores,
            age_column_name=age_column_name,
            psa_column_name=psa_column_name,
            primary_gleason_column_name=primary_gleason_column_name,
            secondary_gleason_column_name=secondary_gleason_column_name,
            clinical_stage_column_name=clinical_stage_column_name,
            number_of_positive_cores_column_name=number_of_positive_cores_column_name,
            number_of_negative_cores_column_name=number_of_negative_cores_column_name
        )

    @staticmethod
    def _get_dict_from_two_columns_of_a_dataframe(
            dataframe: pd.DataFrame,
            keys_column_name: str,
            values_column_name: str
    ) -> Mapping[str, float]:
        """
        Gets a dictionary from two columns of a dataframe. The first column is the keys and the second column is the
        values.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe.
        keys_column_name : str
            The name of the column that contains the keys.
        values_column_name : str
            The name of the column that contains the values.

        Returns
        -------
        dict : Mapping[str, float]
            The dictionary.
        """
        return pd.Series(data=dataframe[values_column_name].values, index=dataframe[keys_column_name]).to_dict()

    @property
    def cores(self):
        """
        Whether the model is for cores or not.

        Returns
        -------
        is_cores : bool
            Whether the model is for cores or not.
        """
        if self.outcome.endswith("(Cores)"):
            return True
        else:
            return False

    @property
    def model_type(self) -> str:
        """
        The type of the model. It is used to determine which model to use for the prediction.

        Returns
        -------
        model_type : str
            The type of the model. It is used to determine which model to use for the prediction.
        """
        model_type = self._variables_coefficients_dataframe["Model Type"].values[0]

        return model_type

    @property
    def variables_coefficients(self) -> Mapping[str, float]:
        """
        Gets the variables values from the dataframe.

        Returns
        -------
        variables_values : Mapping[str, float]
            The variables values.
        """
        variables_values = self._get_dict_from_two_columns_of_a_dataframe(
            dataframe=self._variables_coefficients_dataframe,
            keys_column_name="Variable",
            values_column_name="Value"
        )

        return variables_values

    @property
    def spline_coefficients(self) -> Mapping[str, float]:
        """
        Gets the spline knots values from the dataframe.

        Returns
        -------
        spline_knots_values : Mapping[str, float]
            The spline knots values.
        """
        spline_knots_values = self._get_dict_from_two_columns_of_a_dataframe(
            dataframe=self._splines_coefficients_dataframe,
            keys_column_name="Knot",
            values_column_name="Value"
        )

        return spline_knots_values

    def predict_proba(
            self,
            dataframe: pd.DataFrame,
            number_of_years: Union[np.ndarray, list, float, int] = None
    ) -> np.ndarray:
        """
        Gets the predictions. If the model is survival, the number of years must be given.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe.
        number_of_years : Union[numpy.ndarray, list, float, int], optional
            The number of years. It is used only for survival models.

        Returns
        -------
        predictions : numpy.ndarray
            The predictions.
        """
        if self.model_type == "survival":
            if number_of_years is None:
                raise ValueError("Number of years must be given.")
            else:
                return self.regressor.get_predicted_survival_probability(dataframe, number_of_years)
        elif self.model_type == "logistic":
            return self.regressor.get_predicted_probability(dataframe=dataframe)
        else:
            raise ValueError(f"Model type {self.model_type} doesn't exist.")
