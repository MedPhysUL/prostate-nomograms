import os
from typing import Optional, Union

from .base import Model
from ..enum import ClassificationOutcome, SurvivalOutcome


class MskccPreRadicalProstatectomyNomogram(Model):

    def __init__(
            self,
            outcome: Union[str, ClassificationOutcome, SurvivalOutcome],
            age_column_name: str = "AGE",
            psa_column_name: str = "PSA",
            primary_gleason_column_name: str = "GLEASON_PRIMARY",
            secondary_gleason_column_name: str = "GLEASON_SECONDARY",
            clinical_stage_column_name: str = "CLINICAL_STAGE",
            number_of_positive_cores_column_name: Optional[str] = None,
            number_of_negative_cores_column_name: Optional[str] = None
    ):
        """
        Initializes columns names.

        Parameters
        ----------
        outcome : Union[str, ClassificationOutcome, SurvivalOutcome]
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
        number_of_positive_cores_column_name : str, optional
            Name of the column containing the number of positive cores of the patients.
        number_of_negative_cores_column_name : str, optional
            Name of the column containing the number of negative cores of the patients.
        """
        if outcome in ClassificationOutcome:
            self.outcome = ClassificationOutcome(outcome)
        elif outcome in SurvivalOutcome:
            self.outcome = SurvivalOutcome(outcome)
        else:
            raise ValueError(f"Invalid outcome: {outcome}")

        super().__init__(
            outcome=self.outcome,
            url="https://www.mskcc.org/nomograms/prostate/pre_op/coefficients",
            json_folder_path=os.path.join(os.path.dirname(__file__), "models_coefficients"),
            age_column_name=age_column_name,
            psa_column_name=psa_column_name,
            primary_gleason_column_name=primary_gleason_column_name,
            secondary_gleason_column_name=secondary_gleason_column_name,
            clinical_stage_column_name=clinical_stage_column_name,
            number_of_positive_cores_column_name=number_of_positive_cores_column_name,
            number_of_negative_cores_column_name=number_of_negative_cores_column_name
        )
