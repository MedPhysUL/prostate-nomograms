import pandas as pd
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve

from prostate_cancer_nomograms.statistical_analysis.base.base_performance_evaluation import BasePerformanceEvaluation


class CalibrationCurve(BasePerformanceEvaluation):
    def __init__(self, dataframe: pd.DataFrame, nomogram: str):
        super().__init__(dataframe, nomogram)

    def plot_calibration_curve(self, outcome: str, reverse_outcome: bool = False):
        self.outcome = outcome

        if reverse_outcome:
            pos_label = self.outcome_specific_dataframes_information.value_of_negative_outcome
        else:
            pos_label = self.outcome_specific_dataframes_information.value_of_positive_outcome

        prob_true, prob_pred = calibration_curve(
            y_true=self.y_true,
            y_prob=self.y_score,
            pos_label=pos_label,
            n_bins=8,
            normalize=True,
            strategy="quantile"
        )

        plt.plot(prob_pred, prob_true, color='darkorange', lw=2)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'Calibration curve \n'
                  f'{self.nomogram} - {self.outcome}')
        plt.show()
