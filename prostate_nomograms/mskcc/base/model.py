from typing import Mapping, Optional, Union

import numpy as np
import pandas as pd

from ...enum import SurvivalOutcome
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
        self.url = url
        self.json_folder_path = json_folder_path

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

        if self.is_predicting_death:
            self._regressor_as_variable = self._create_regressor_as_variable()
        else:
            self._regressor_as_variable = None

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
    def is_predicting_death(self):
        """
        Whether the model is predicting death or not.

        Returns
        -------
        is_death : bool
            Whether the model is for predicting death or not.
        """
        if "Death" in self.outcome:
            return True
        else:
            return False

    @staticmethod
    def _map_death_model_to_bcr_outcome() -> dict:
        """
        Map death model to the corresponding bcr outcome used for its prediction computation.

        Returns
        -------
        mapping : dict
            Map from the death model to the corresponding bcr outcome.
        """
        return {
            SurvivalOutcome.PREOPERATIVE_PROSTATE_CANCER_DEATH: SurvivalOutcome.PREOPERATIVE_BCR,
            SurvivalOutcome.PREOPERATIVE_PROSTATE_CANCER_DEATH_CORES: SurvivalOutcome.PREOPERATIVE_BCR_CORES
        }

    def _create_regressor_as_variable(self) -> SurvivalRegression:
        """
        Creates the regressor as a variable.

        Returns
        -------
        model : SurvivalRegression
            The regressor as a variable.
        """
        outcome = self._map_death_model_to_bcr_outcome()[self.outcome]
        return Model(
            outcome=outcome,
            url=self.url,
            json_folder_path=self.json_folder_path,
            age_column_name=self.regressor.age_column_name,
            psa_column_name=self.regressor.psa_column_name,
            primary_gleason_column_name=self.regressor.primary_gleason_column_name,
            secondary_gleason_column_name=self.regressor.secondary_gleason_column_name,
            clinical_stage_column_name=self.regressor.clinical_stage_column_name,
            number_of_positive_cores_column_name=self.regressor.number_of_positive_cores,
            number_of_negative_cores_column_name=self.regressor.number_of_negative_cores
        ).regressor

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
            number_of_months: Union[np.ndarray, list, float, int] = None
    ) -> np.ndarray:
        """
        Gets the predictions. If the model is survival, the number of years must be given.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe.
        number_of_months : Union[numpy.ndarray, list, float, int], optional
            The number of months. It is used only for survival models.

        Returns
        -------
        predictions : numpy.ndarray
            The predictions.
        """
        if self.model_type == "survival":
            if number_of_months is None:
                raise ValueError("Number of months must be given.")
            else:
                return self.regressor.get_predicted_survival_probability(
                    dataframe,
                    number_of_months,
                    self._regressor_as_variable
                )
        elif self.model_type == "logistic":
            return self.regressor.get_predicted_probability(
                dataframe,
                self._regressor_as_variable
            )
        else:
            raise ValueError(f"Model type {self.model_type} doesn't exist.")

    def predict_risk(
            self,
            dataframe: pd.DataFrame
    ) -> np.ndarray:
        """
        Gets the risk predictions.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            The dataframe.

        Returns
        -------
        predictions : numpy.ndarray
            The predictions.
        """
        if self.model_type == "survival":
            return self.regressor.get_predicted_risk(dataframe, self._regressor_as_variable)
        elif self.model_type == "logistic":
            raise ValueError("Logistic models don't have risk predictions.")
        else:
            raise ValueError(f"Model type {self.model_type} doesn't exist.")
