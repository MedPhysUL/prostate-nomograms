from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from ..enum import Outcome, SurvivalOutcome
from .base import LogisticRegression, SurvivalRegression


class CAPRAModel:
    """
    CAPRA nomogram. See
    https://urology.ucsf.edu/research/cancer/prostate-cancer-risk-assessment-and-the-ucsf-capra-score.
    """

    def __init__(
            self,
            outcome: Union[str, Outcome],
            target_column_name: Optional[str] = None,
            event_indicator_column_name: Optional[str] = None,
            event_time_column_name: Optional[str] = None,
            age_column_name: str = "AGE",
            psa_column_name: str = "PSA",
            primary_gleason_column_name: str = "GLEASON_PRIMARY",
            secondary_gleason_column_name: str = "GLEASON_SECONDARY",
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
        positive_cores_percentage_column_name : str, optional
            Name of the column containing the number of positive cores of the patients.
        random_state : int, optional
            Random state.
        """
        self.outcome = Outcome(outcome)
        self.target_column_name = target_column_name
        self.event_indicator_column_name = event_indicator_column_name
        self.event_time_column_name = event_time_column_name
        self.age_column_name = age_column_name
        self.psa_column_name = psa_column_name
        self.primary_gleason_column_name = primary_gleason_column_name
        self.secondary_gleason_column_name = secondary_gleason_column_name
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

    def _get_age_score(self, data_dict: dict) -> np.ndarray:
        """
        Gets the age score.

        Parameters
        ----------
        data_dict : dict
            Dictionary containing the data of the patients.

        Returns
        -------
        age_score : np.ndarray
            Age score.
        """
        age = np.array(data_dict[self.age_column_name])
        age_score = np.zeros_like(age, dtype=float)

        age_score[age < 50] = 0
        age_score[age >= 50] = 1

        return age_score

    def _get_psa_score(self, data_dict: dict) -> np.ndarray:
        """
        Gets the PSA score.

        Parameters
        ----------
        data_dict : dict
            Dictionary containing the data of the patients.

        Returns
        -------
        psa_score : np.ndarray
            PSA score.
        """
        psa = np.array(data_dict[self.psa_column_name])
        psa_score = np.zeros_like(psa, dtype=float)

        psa_score[psa < 6] = 0
        psa_score[(6 <= psa) & (psa < 10)] = 1
        psa_score[(10 <= psa) & (psa < 20)] = 2
        psa_score[(20 <= psa) & (psa < 30)] = 3
        psa_score[psa >= 30] = 4

        return psa_score

    def _get_gleason_score(self, data_dict: dict) -> np.ndarray:
        """
        Gets the Gleason score.

        Parameters
        ----------
        data_dict : dict
            Dictionary containing the data of the patients.

        Returns
        -------
        gleason_score : np.ndarray
            Gleason score.
        """
        primary_gleason = np.array(data_dict[self.primary_gleason_column_name])
        secondary_gleason = np.array(data_dict[self.secondary_gleason_column_name])
        total_gleason_score = primary_gleason + secondary_gleason

        gleason_score = np.zeros_like(total_gleason_score, dtype=float)

        gleason_score[(secondary_gleason == 4) | (secondary_gleason == 5)] = 1
        gleason_score[(primary_gleason == 4) | (primary_gleason == 5)] = 3

        return gleason_score

    def _get_clinical_stage_score(self, data_dict: dict) -> np.ndarray:
        """
        Gets the clinical stage score.

        Parameters
        ----------
        data_dict : dict
            Dictionary containing the data of the patients.

        Returns
        -------
        clinical_stage_score : np.ndarray
            Clinical stage score.
        """
        clinical_tumor_stage = data_dict[self.clinical_stage_column_name]

        clinical_stage_score = np.zeros_like(clinical_tumor_stage, dtype=float)
        clinical_stage_score[list(map("T3a".__eq__, clinical_tumor_stage))] = 1

        return clinical_stage_score

    def _get_positive_cores_score(self, data_dict: dict) -> np.ndarray:
        """
        Gets the positive cores score.

        Parameters
        ----------
        data_dict : dict
            Dictionary containing the data of the patients.

        Returns
        -------
        positive_cores_score : np.ndarray
            Positive cores score.
        """
        if self.positive_cores_percentage_column_name:
            positive_cores_percentage = np.array(data_dict[self.positive_cores_percentage_column_name], dtype=float)

            positive_cores_score = np.zeros_like(positive_cores_percentage, dtype=float)
            positive_cores_score[positive_cores_percentage >= 34] = 1

            return positive_cores_percentage
        else:
            return np.zeros_like(data_dict[self.age_column_name], dtype=float)

    def get_capra_score(self, dataframe: pd.DataFrame) -> np.ndarray:
        """
        Gets the CAPRA score.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataframe containing the data of the patients.

        Returns
        -------
        capra_score : np.ndarray
            CAPRA score.
        """
        data_dict = dataframe.to_dict(orient="list")

        capra_score = self._get_age_score(data_dict)
        capra_score += self._get_psa_score(data_dict)
        capra_score += self._get_gleason_score(data_dict)
        capra_score += self._get_clinical_stage_score(data_dict)

        if self.cores:
            capra_score += self._get_positive_cores_score(data_dict)

        return capra_score

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
        capra_score = self.get_capra_score(dataset)

        if self.model_type == "survival":
            self.regressor.fit(
                capra_score,
                np.array(dataset[self.event_indicator_column_name], dtype=bool),
                np.array(dataset[self.event_time_column_name], dtype=float)
            )
        else:
            self.regressor.fit(
                capra_score,
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

        capra_score = self.get_capra_score(dataframe)
        if self.model_type == "survival":
            if number_of_months is None:
                raise ValueError("Number of months must be given.")
            else:
                return self.regressor.get_predicted_survival_probability(capra_score, number_of_months)
        elif self.model_type == "logistic":
            return self.regressor.get_predicted_probability(capra_score)
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
            capra_score = self.get_capra_score(dataframe)
            return self.regressor.get_predicted_risk(capra_score)
        elif self.model_type == "logistic":
            raise ValueError("Logistic models don't have risk predictions.")
        else:
            raise ValueError(f"Model type {self.model_type} doesn't exist.")

    def show_histogram(self, dataframe: pd.DataFrame) -> None:
        """
        Shows the histogram of the CAPRA score.

        Parameters
        ----------
        dataframe : pd.DataFrame
            Dataframe containing the data of the patients.
        """
        plt.hist(self.get_capra_score(dataframe), bins=20)
        plt.show()
