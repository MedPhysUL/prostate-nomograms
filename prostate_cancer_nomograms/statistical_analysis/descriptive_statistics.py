import numpy as np
import pandas as pd
from scipy import stats

from .base_statistics import BaseStatistics


class DescriptiveStatistics(BaseStatistics):

    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)

    def get_descriptive_stats_dataframe_from_given_columns(self, list_of_columns: list) -> pd.DataFrame:
        reduced_dataset = self.dataframe[list_of_columns]
        descriptive_stats_dataframe = reduced_dataset.describe().transpose().round(decimals=1)
        descriptive_stats_dataframe.insert(loc=0, column="Variable", value=descriptive_stats_dataframe.index)

        return descriptive_stats_dataframe

    @staticmethod
    def _get_p_value_from_mann_whitney_u_test(
            column_name: str,
            negative_outcome_dataframe: pd.DataFrame,
            positive_outcome_dataframe: pd.DataFrame
    ) -> float:
        _, p_value = stats.mannwhitneyu(
            x=negative_outcome_dataframe[column_name].dropna(),
            y=positive_outcome_dataframe[column_name].dropna()
        )

        return p_value

    @staticmethod
    def _get_dataframe_with_strings_converted_to_numbers_in_given_column(
            column_name: str,
            dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        if dataframe[column_name].dtype == object:
            numeric_value_mask = [value.replace(".", "", 1).isdigit() for value in dataframe[column_name].values]

            if any(numeric_value_mask):
                dataframe[column_name].values[not numeric_value_mask] = np.nan
                dataframe[column_name].values[numeric_value_mask] = [
                    float(value) for value in dataframe[column_name].values[numeric_value_mask]
                ]

                dataframe[column_name] = pd.to_numeric(dataframe[column_name], errors='coerce')
            else:
                pass
        else:
            pass

        return dataframe

    def _get_dataframes_subset_from_given_columns(self, list_of_columns: list, outcome: str):
        self.outcome = outcome

        negative_outcome_dataframe_subset = self.outcome_specific_dataframes.negative_outcome_dataframe[list_of_columns]
        positive_outcome_dataframe_subset = self.outcome_specific_dataframes.positive_outcome_dataframe[list_of_columns]

        for column in list_of_columns:
            negative_outcome_dataframe_subset = self._get_dataframe_with_strings_converted_to_numbers_in_given_column(
                column_name=column,
                dataframe=negative_outcome_dataframe_subset
            )
            positive_outcome_dataframe_subset = self._get_dataframe_with_strings_converted_to_numbers_in_given_column(
                column_name=column,
                dataframe=positive_outcome_dataframe_subset
            )

        outcome_specific_dataframes = self.OutcomeDataFrames(
            negative_outcome_dataframe=negative_outcome_dataframe_subset,
            positive_outcome_dataframe=positive_outcome_dataframe_subset,
        )

        return outcome_specific_dataframes

    def get_descriptive_stats_dataframe_from_specific_outcome(
            self,
            list_of_columns: list,
            outcome: str
    ) -> pd.DataFrame:
        outcome_specific_dataframes = self._get_dataframes_subset_from_given_columns(
            list_of_columns=list_of_columns,
            outcome=outcome
        )

        negative_outcome_dataframe = outcome_specific_dataframes.negative_outcome_dataframe
        positive_outcome_dataframe = outcome_specific_dataframes.positive_outcome_dataframe

        stats_negative_outcome = negative_outcome_dataframe.describe().transpose().round(decimals=2).reset_index()
        stats_positive_outcome = positive_outcome_dataframe.describe().transpose().round(decimals=2).reset_index()

        stats_negative_outcome.insert(
            loc=0,
            column='Level',
            value=self.outcome_specific_dataframes_information.value_of_negative_outcome
        )

        stats_positive_outcome.insert(
            loc=0,
            column='Level',
            value=self.outcome_specific_dataframes_information.value_of_positive_outcome
        )

        concat_df = pd.concat([stats_negative_outcome, stats_positive_outcome]).sort_index().set_index('index')

        concat_df.index = ["" if idx % 2 != 0 else label for idx, label in enumerate(concat_df.index)]
        concat_df.insert(loc=0, column="Variable", value=concat_df.index)

        p_values = []
        for idx, label in enumerate(concat_df.index):
            if idx % 2 != 0:
                p_value = ""
            else:
                p_value = self._get_p_value_from_mann_whitney_u_test(
                    column_name=label,
                    negative_outcome_dataframe=negative_outcome_dataframe,
                    positive_outcome_dataframe=positive_outcome_dataframe
                )

            p_values.append(p_value)

        concat_df["p-value"] = p_values

        return concat_df

    def _get_count_dataframe(self, variable_name, outcome_specific: bool = False) -> pd.DataFrame:
        if outcome_specific:
            data = [
                self.negative_outcome_dataframe[variable_name].value_counts(),
                self.positive_outcome_dataframe[variable_name].value_counts()
            ]

            count_dataframe_int: pd.DataFrame(dtype=int) = pd.concat(data, axis=1).fillna(0).applymap(int)
            count_dataframe_str: pd.DataFrame(dtype=str) = count_dataframe_int.applymap(str)

            for column_idx, _ in enumerate(count_dataframe_int.columns):
                column_sum = count_dataframe_int.iloc[:, column_idx].sum()
                count_dataframe_str.iloc[:, column_idx] = count_dataframe_str.iloc[:, column_idx] + f"/{column_sum}"
        else:
            count_dataframe_int = self.dataframe[variable_name].value_counts().fillna(0).apply(int)
            count_dataframe_str: pd.DataFrame(dtype=str) = count_dataframe_int.apply(str)

            column_sum = count_dataframe_int.sum()
            count_dataframe_str = count_dataframe_str + f"/{column_sum}"

        return count_dataframe_str

    def _get_percentage_dataframe(self, variable_name, outcome_specific: bool = False) -> pd.DataFrame:
        if outcome_specific:
            data = [
                round(self.negative_outcome_dataframe[variable_name].value_counts(normalize=True)*100, ndigits=1),
                round(self.positive_outcome_dataframe[variable_name].value_counts(normalize=True)*100, ndigits=1)
            ]

            percentage_dataframe: pd.DataFrame(dtype=int) = pd.concat(data, axis=1).fillna(0)
        else:
            percentage_dataframe = round(self.dataframe[variable_name].value_counts(normalize=True)*100, ndigits=1)

        return percentage_dataframe

    def _get_count_and_percentage_dataframe_from_variable_name(
            self,
            variable_name: str,
            outcome_specific: bool = False
    ) -> pd.DataFrame:
        count_and_percentage_dataframe = pd.merge(
            left=self._get_count_dataframe(variable_name=variable_name, outcome_specific=outcome_specific),
            right=self._get_percentage_dataframe(variable_name=variable_name, outcome_specific=outcome_specific),
            left_index=True,
            right_index=True
        )

        return count_and_percentage_dataframe

    @staticmethod
    def _get_frequency_table_with_concatenated_list(
            frequency_table: pd.DataFrame,
            values: list,
            first_column: bool = False
    ) -> pd.DataFrame:
        series = pd.Series(data=values, index=frequency_table.index)

        if first_column:
            data = [series, frequency_table]
        else:
            data = [frequency_table, series]

        frequency_table = pd.concat(data, axis=1, ignore_index=True)

        return frequency_table

    def get_frequency_table(self, list_of_columns: list) -> pd.DataFrame:
        dataframes = []
        for variable_idx, variable_name in enumerate(list_of_columns):
            frequency_table = self._get_count_and_percentage_dataframe_from_variable_name(
                variable_name=variable_name,
                outcome_specific=False
            )

            frequency_table = self._get_frequency_table_with_concatenated_list(
                frequency_table=frequency_table,
                values=list(frequency_table.index),
                first_column=True
            )

            number_of_levels = len(frequency_table.index)
            variable = [""] * number_of_levels
            variable[0] = variable_name
            frequency_table = self._get_frequency_table_with_concatenated_list(
                frequency_table=frequency_table,
                values=variable,
                first_column=True
            )

            dataframes.append(frequency_table)

        dataframe = pd.concat(dataframes)
        columns = ["Variable", "Level", "n", "%"]
        dataframe.columns = columns

        return dataframe

    def _get_outcome_dependent_frequency_table(self, column_name: str) -> pd.DataFrame:
        result = pd.concat(
            [
                self.outcome_specific_dataframes.negative_outcome_dataframe[column_name].value_counts(),
                self.outcome_specific_dataframes.positive_outcome_dataframe[column_name].value_counts()
            ],
            axis=1
        ).fillna(0)

        return result

    def _get_p_value_from_chi2_test_on_frequency_table(self, column_name: str) -> float:
        result = self._get_outcome_dependent_frequency_table(column_name=column_name)
        chi2, p_value, dof, expected = stats.chi2_contingency(observed=result)

        return p_value

    def get_frequency_table_and_test_on_proportions(self, list_of_columns: list, outcome: str) -> pd.DataFrame:
        self.outcome = outcome

        dataframes = []
        for variable_idx, variable_name in enumerate(list_of_columns):
            frequency_table = self._get_count_and_percentage_dataframe_from_variable_name(
                variable_name=variable_name,
                outcome_specific=True
            )

            number_of_levels = len(frequency_table.index)

            p_value = [""] * number_of_levels
            p_value[0] = str(round(self._get_p_value_from_chi2_test_on_frequency_table(column_name=variable_name), ndigits=4))
            frequency_table = self._get_frequency_table_with_concatenated_list(
                frequency_table=frequency_table,
                values=p_value
            )

            frequency_table = self._get_frequency_table_with_concatenated_list(
                frequency_table=frequency_table,
                values=list(frequency_table.index),
                first_column=True
            )

            variable = [""] * number_of_levels
            variable[0] = variable_name
            frequency_table = self._get_frequency_table_with_concatenated_list(
                frequency_table=frequency_table,
                values=variable,
                first_column=True
            )

            frequency_table = frequency_table[[0, 1, 2, 4, 3, 5, 6]]

            dataframes.append(frequency_table)

        dataframe = pd.concat(dataframes)
        columns = ["Variable", "Level", "Negative n/N", "Negative %", "Positive n/N", "Positive %", "p-value"]
        dataframe.columns = columns

        return dataframe
