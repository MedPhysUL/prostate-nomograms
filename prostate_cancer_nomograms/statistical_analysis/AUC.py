import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc

from .base_statistics import BaseStatistics


class AUC(BaseStatistics):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

    def _calculate_auc_curve(self, outcome: str):
        self.outcome = outcome

        outcome_column_name = self.outcome_specific_dataframes_information.outcome_column_name_in_dataframe
        probability_column_name = self.outcome_specific_dataframes_information.probability_column_name_in_dataframe
        value_of_positive_outcome = self.outcome_specific_dataframes_information.value_of_positive_outcome

        print(self.outcome_specific_dataframes_information)

        fpr, tpr, thresholds = roc_curve(
            y_true=np.array(self.dataframe[outcome_column_name]),
            y_score=np.array(self.dataframe[probability_column_name]),
            pos_label=value_of_positive_outcome
        )

        return fpr, tpr, thresholds

    @staticmethod
    def get_auc_score(fpr, tpr):
        auc_score = auc(
            x=fpr,
            y=tpr
        )

        return auc_score

    def plot_auc(self, outcome: str):
        fpr, tpr, thresholds = self._calculate_auc_curve(outcome=outcome)

        plt.plot(fpr, tpr, color='darkorange', lw=2)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'Receiver operating characteristic (AUC = {self.get_auc_score(fpr=fpr, tpr=tpr): .3f})')
        plt.show()
