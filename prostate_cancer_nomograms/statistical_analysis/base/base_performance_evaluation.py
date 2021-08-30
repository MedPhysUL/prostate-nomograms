import pandas as pd
import numpy as np

from prostate_cancer_nomograms.statistical_analysis.base.base_statistics import BaseStatistics
from prostate_cancer_nomograms.statistical_analysis.base.logistic_regression import CustomLogisticRegression
from prostate_cancer_nomograms.nomograms import Nomograms


class BasePerformanceEvaluation(BaseStatistics):

    def __init__(self, dataframe: pd.DataFrame, nomogram: str):
        super().__init__(dataframe)
        self.nomogram = nomogram

    @property
    def nomogram(self) -> str:
        return self._nomogram

    @nomogram.setter
    def nomogram(self, nomogram: str):
        if nomogram in Nomograms.__members__:
            self._nomogram = nomogram
        else:
            raise ValueError(f"Given member {nomogram} is not allowed. Allowed members of {Nomograms} are "
                             f"{list(Nomograms.__members__)}.")

    @property
    def predicted_probability(self):
        outcome_column_name = self.outcome_specific_dataframes_information.outcome_column_name_in_dataframe
        value_of_positive_outcome = self.outcome_specific_dataframes_information.value_of_positive_outcome

        if self.nomogram == "CAPRA":
            column_name = self.outcome_specific_dataframes_information.nomograms.CAPRA

            logistic_regression = CustomLogisticRegression(
                x=self.dataframe[column_name],
                y=self.dataframe[outcome_column_name],
                positive_label=value_of_positive_outcome
            )

            return logistic_regression.predicted_probability
        else:
            column_name = getattr(self.outcome_specific_dataframes_information.nomograms, self.nomogram)

            return np.array(self.dataframe[column_name])
