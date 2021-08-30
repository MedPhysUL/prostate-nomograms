import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, auc

from prostate_cancer_nomograms.statistical_analysis.base.base_performance_evaluation import BasePerformanceEvaluation


class AUC(BasePerformanceEvaluation):
    def __init__(self, dataframe: pd.DataFrame, nomogram: str):
        super().__init__(dataframe, nomogram)

    def _calculate_auc_curve(self, outcome: str):
        self.outcome = outcome

        outcome_column_name = self.outcome_specific_dataframes_information.outcome_column_name_in_dataframe
        value_of_positive_outcome = self.outcome_specific_dataframes_information.value_of_positive_outcome

        fpr, tpr, thresholds = roc_curve(
            y_true=np.array(self.dataframe[outcome_column_name]),
            y_score=self.predicted_probability,
            pos_label=value_of_positive_outcome
        )

        return fpr, tpr, thresholds

    @staticmethod
    def _get_auc_score(fpr, tpr):
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
        plt.title(f'Receiver operating characteristic (AUC = {self._get_auc_score(fpr=fpr, tpr=tpr): .3f})')
        plt.show()
