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
        descriptive_stats_dataframe = reduced_dataset.describe().transpose().round(decimals=1)

        return descriptive_stats_dataframe

    def get_frequency_table(self, list_of_columns: list):
        dataframe = pd.DataFrame(columns=["Variable", "Level", "n", "%"])

        number_of_levels = 0
        for variable_idx, variable_name in enumerate(list_of_columns):
            value_counts: pd.Series = self.dataset[variable_name].value_counts()
            ratio_counts: pd.Series = self.dataset[variable_name].value_counts(normalize=True)

            levels = list(value_counts.index)
            counts = value_counts.to_list()
            percentage_counts = round(ratio_counts*100, ndigits=1).to_list()

            dataframe.loc[number_of_levels] = [variable_name, levels[0], counts[0], percentage_counts[0]]
            for relative_level_idx, (level, count, percent) in enumerate(
                    zip(levels[1:], counts[1:], percentage_counts[1:]),
                    start=1
            ):
                true_level_idx = relative_level_idx + number_of_levels
                dataframe.loc[true_level_idx] = ["", level, count, percent]

            number_of_levels += len(levels)

        return dataframe

    def get_frequency_table_and_test_on_proportions(self, list_of_columns: list):
        dataframe = pd.DataFrame(columns=["Variable", "Level", "n/N", "%", "n/N", "%", "p-value"])

        number_of_levels = 0
        for variable_idx, variable_name in enumerate(list_of_columns):
            value_counts_pn0: pd.Series = self.dataset_pN0[variable_name].value_counts()
            ratio_counts_pn0: pd.Series = self.dataset_pN0[variable_name].value_counts(normalize=True)

            levels_pn0 = list(value_counts_pn0.index)
            counts_pn0 = value_counts_pn0.to_list()
            percentage_counts_pn0 = round(ratio_counts_pn0 * 100, ndigits=1).to_list()

            value_counts_pn1: pd.Series = self.dataset_pN1[variable_name].value_counts()
            ratio_counts_pn1: pd.Series = self.dataset_pN1[variable_name].value_counts(normalize=True)

            counts_pn1 = value_counts_pn1.to_list()
            percentage_counts_pn1 = round(ratio_counts_pn1 * 100, ndigits=1).to_list()

            p_value = self.chi2_test_on_frequency_table(column_name=variable_name)

            dataframe.loc[number_of_levels] = [
                variable_name,
                levels_pn0[0],
                counts_pn0[0],
                percentage_counts_pn0[0],
                counts_pn1[0],
                percentage_counts_pn1[0],
                p_value
            ]

            for relative_level_idx, (level, count_pn0, percent_pn0, count_pn1, percent_pn1) in enumerate(
                    zip(levels_pn0[1:], counts_pn0[1:], percentage_counts_pn0[1:], counts_pn0[1:],
                        percentage_counts_pn1[1:]),
                    start=1
            ):
                true_level_idx = relative_level_idx + number_of_levels
                dataframe.loc[true_level_idx] = ["", level, count_pn0, percent_pn0, count_pn1, percent_pn1, ""]

            number_of_levels += len(levels_pn0)

        return dataframe

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

        return p_value

    def mannwhitneyu_test(self, column_name: str):
        U1, p = stats.mannwhitneyu(
            x=self.dataset_pN0[column_name],
            y=self.dataset_pN1[column_name]
        )

        print(p)
