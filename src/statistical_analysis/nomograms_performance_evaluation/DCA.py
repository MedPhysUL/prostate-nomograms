import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from prostate_cancer_nomograms.statistical_analysis.base.base_performance_evaluation import BasePerformanceEvaluation
from .decision_curve_analysis import DecisionCurveAnalysis


class DCA(BasePerformanceEvaluation):
    def __init__(self, dataframe: pd.DataFrame, nomogram: str):
        super().__init__(dataframe, nomogram)

    @property
    def binary_outcome_array(self):
        binary_outcome = pd.DataFrame(data=np.zeros(len(self.y.index)), index=self.y.index)
        positive_value_idx = self.y.index[self.y == self.positive_label].tolist()
        binary_outcome.loc[positive_value_idx] = 1
        binary_outcome_array = np.array(binary_outcome).ravel()

        return binary_outcome_array

    def plot_dca(self, outcome: str):
        self.outcome = outcome

        df = pd.DataFrame(index=self.dataframe.index)
        df["outcome"] = self.y_true
        df["predictors"] = self.y_score

        df_outcome = df["outcome"]
        binary_outcome = pd.DataFrame(data=np.zeros(len(df_outcome.index)), index=df_outcome.index)
        positive_value_idx = df_outcome.index[
            df_outcome == self.outcome_specific_dataframes_information.value_of_positive_outcome].tolist()
        binary_outcome.loc[positive_value_idx] = 1

        df["outcome"] = binary_outcome

        dca = DecisionCurveAnalysis(
            data=df,
            outcome="outcome",
            predictors="predictors"
        )

        dca.run()
        dca.plot_net_benefit()
        plt.show()
