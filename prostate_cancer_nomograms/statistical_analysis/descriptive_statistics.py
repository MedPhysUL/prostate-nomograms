import pandas as pd
from scipy import stats


class DescriptiveStatistics:

    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset

    @property
    def dataset_pN0(self):
        return self.dataset[self.dataset["pN"] == "pN0"]

    @property
    def dataset_pN1(self):
        return self.dataset[self.dataset["pN"] == "pN1"]

    def get_descriptive_stats_dataframe_from_given_columns(self, list_of_columns: list) -> pd.DataFrame:
        reduced_dataset = self.dataset[list_of_columns]

        return reduced_dataset.describe()

    def print_frequency_table(self, list_of_columns: list):
        for column_name in list_of_columns:
            print(self.dataset[column_name].value_counts())

    def print_pN0_frequency_table(self, list_of_columns: list):
        for column_name in list_of_columns:
            print(self.dataset_pN0[column_name].value_counts())

    def print_pN1_frequency_table(self, list_of_columns: list):
        for column_name in list_of_columns:
            print(self.dataset_pN1[column_name].value_counts())

    def pN_frequency_table(self, column_name: str):
        result = pd.concat(
            [self.dataset_pN0[column_name].value_counts(), self.dataset_pN1[column_name].value_counts()],
            axis=1
        )
        result = result.fillna(0)
        print(result)

        return result

    def chi2_test_on_frequency_table(self, column_name: str):
        result = self.pN_frequency_table(column_name=column_name)
        chi2, p_value, dof, expected = stats.chi2_contingency(observed=result)

        print(p_value)

    def mannwhitneyu_test(self, column_name: str):
        U1, p = stats.mannwhitneyu(
            x=self.dataset_pN0[column_name],
            y=self.dataset_pN1[column_name]
        )

        print(p)
