from typing import List, Optional, Union

import pandas as pd
import numpy as np

from ..enum import ClassificationOutcome, SurvivalOutcome
from .base import LogisticRegression, SurvivalRegression


class CustomNomogram:
    """
    Custom model. It can be used to create a nomogram with a custom model.
    """

    def __init__(
            self,
            outcome: Union[str, ClassificationOutcome, SurvivalOutcome],
            target_column_name: Optional[str] = None,
            event_indicator_column_name: Optional[str] = None,
            event_time_column_name: Optional[str] = None,
            age_column_name: str = "AGE",
            psa_column_name: str = "PSA",
            primary_gleason_column_name: str = "GLEASON_PRIMARY",
            secondary_gleason_column_name: str = "GLEASON_SECONDARY",
            global_gleason_column_name: str = "GLEASON_GLOBAL",
            clinical_stage_column_name: str = "CLINICAL_STAGE",
            positive_cores_percentage_column_name: Optional[str] = None,
            random_state: int = 0
    ):
        """
        Initializes columns names.

        Parameters
        ----------
        outcome : Optional[Union[str, Outcome]]
            Name of the outcome.
        target_column_name : Optional[str]
            Name of the column containing the target of the patients.
        event_indicator_column_name : Optional[str]
            Name of the column containing the event indicator of the patients.
        event_time_column_name : Optional[str]
            Name of the column containing the event time of the patients.
        age_column_name : str
            Name of the column containing the age of the patients.
        psa_column_name : str
            Name of the column containing the PSA of the patients.
        primary_gleason_column_name : str
            Name of the column containing the primary Gleason score of the patients.
        secondary_gleason_column_name : str
            Name of the column containing the secondary Gleason score of the patients.
        global_gleason_column_name : str
            Name of the column containing the global Gleason score of the patients.
        clinical_stage_column_name : str
            Name of the column containing the clinical stage of the patients.
        positive_cores_percentage_column_name : str, optional
            Name of the column containing the number of positive cores of the patients.
        random_state : int, optional
            Random state.
        """
        if outcome in ClassificationOutcome:
            self.outcome = ClassificationOutcome(outcome)
        elif outcome in SurvivalOutcome:
            self.outcome = SurvivalOutcome(outcome)
        else:
            raise ValueError(f"Invalid outcome: {outcome}")

        self.target_column_name = target_column_name
        self.event_indicator_column_name = event_indicator_column_name
        self.event_time_column_name = event_time_column_name
        self.age_column_name = age_column_name
        self.psa_column_name = psa_column_name
        self.primary_gleason_column_name = primary_gleason_column_name
        self.secondary_gleason_column_name = secondary_gleason_column_name
        self.global_gleason_column_name = global_gleason_column_name
        self.clinical_stage_column_name = clinical_stage_column_name
        self.positive_cores_percentage_column_name = positive_cores_percentage_column_name
        self._is_fitted = False

        if self.model_type == "survival":
            assert self.event_indicator_column_name is not None, (
                "Event indicator column name must be specified for survival models."
            )
            assert self.event_time_column_name is not None, (
                "Event time column name must be specified for survival models."
            )
            regressor_constructor = SurvivalRegression
        elif self.model_type == "logistic":
            assert self.target_column_name is not None, (
                "Target column name must be specified for logistic models."
            )
            regressor_constructor = LogisticRegression
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

        self.regressor = regressor_constructor(random_state=random_state)

    @property
    def model_type(self) -> str:
        """
        The type of the model. It is used to determine which model to use for the prediction.

        Returns
        -------
        model_type : str
            The type of the model. It is used to determine which model to use for the prediction.
        """
        if self.outcome in list(SurvivalOutcome):
            return "survival"
        else:
            return "logistic"

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
    def columns(self) -> List[str]:
        """
        Returns the columns of the model.

        Returns
        -------
        columns : List[str]
            The columns of the model.
        """
        columns = [
            self.age_column_name,
            self.psa_column_name,
            self.primary_gleason_column_name,
            self.secondary_gleason_column_name,
            self.global_gleason_column_name,
            self.clinical_stage_column_name
        ]

        if self.cores:
            columns.append(self.positive_cores_percentage_column_name)

        return columns

    def get_features(self, dataframe: pd.DataFrame) -> np.ndarray:
        """
        Returns the features of the patients.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataframe containing the data of the patients.

        Returns
        -------
        features : np.ndarray
            The features of the patients.
        """
        dataframe = dataframe[self.columns]
        return np.array(dataframe)

    def fit(
            self,
            dataset: pd.DataFrame
    ):
        """
        Fits the model.

        Parameters
        ----------
        dataset : pd.DataFrame
            Dataframe containing the data of the patients.
        """
        features = self.get_features(dataset)
        if self.model_type == "survival":
            self.regressor.fit(
                features,
                np.array(dataset[self.event_indicator_column_name], dtype=bool),
                np.array(dataset[self.event_time_column_name], dtype=float)
            )
        else:
            self.regressor.fit(
                features,
                np.array(dataset[self.target_column_name])
            )

        self._is_fitted = True

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
        assert self._is_fitted, "Model must be fitted first."

        features = self.get_features(dataframe)
        if self.model_type == "survival":
            if number_of_months is None:
                raise ValueError("Number of months must be given.")
            else:
                return self.regressor.get_predicted_survival_probability(features, number_of_months)
        elif self.model_type == "logistic":
            return self.regressor.get_predicted_probability(features)
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
            features = self.get_features(dataframe)
            return self.regressor.get_predicted_risk(features)
        elif self.model_type == "logistic":
            raise ValueError("Logistic models don't have risk predictions.")
        else:
            raise ValueError(f"Model type {self.model_type} doesn't exist.")
