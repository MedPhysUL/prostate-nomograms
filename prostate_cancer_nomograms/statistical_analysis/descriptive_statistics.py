import enum

import numpy as np
import pandas as pd
from scipy import stats
from typing import NamedTuple


class OutcomeDataFrameInformation(NamedTuple):
    column_name_in_dataframe: str
    value_of_negative_outcome: str
    value_of_positive_outcome: str


LYMPH_NODE_INFO = OutcomeDataFrameInformation(
    column_name_in_dataframe="pN",
    value_of_negative_outcome="pN0",
    value_of_positive_outcome="pN1"
)


class Outcomes(enum.Enum):
    LYMPH_NODE = LYMPH_NODE_INFO


class DescriptiveStatistics:

    class OutcomeDataFrames(NamedTuple):
        negative_outcome_dataframe: pd.DataFrame
        positive_outcome_dataframe: pd.DataFrame

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self._outcome = None

    @property
    def outcome(self):
        return self._outcome

    @outcome.setter
    def outcome(self, outcome: str):
        if outcome in Outcomes.__members__:
            self._outcome = outcome
        else:
            raise ValueError(f"Given member {outcome} is not allowed. Allowed members of {Outcomes} are "
                             f"{list(Outcomes.__members__)}.")

    @property
    def outcome_specific_dataframes_information(self):
        return Outcomes[self.outcome].value

    @property
    def outcome_specific_dataframes(self):
        column_name = self.outcome_specific_dataframes_information.column_name_in_dataframe
        value_of_negative_outcome = self.outcome_specific_dataframes_information.value_of_negative_outcome
        value_of_positive_outcome = self.outcome_specific_dataframes_information.value_of_positive_outcome

        outcome_specific_dataframes = self.OutcomeDataFrames(
            negative_outcome_dataframe=self.dataframe[self.dataframe[column_name] == value_of_negative_outcome],
            positive_outcome_dataframe=self.dataframe[self.dataframe[column_name] == value_of_positive_outcome],
        )

        return outcome_specific_dataframes

    def get_dataframe_with_strings_converted_to_nan_in_given_column(
            self,
            column_name: str,
            dataframe: pd.DataFrame
    ):
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

    def get_dataframes_subset_from_given_columns(self, list_of_columns: list, outcome: str):
        self.outcome = outcome

        negative_outcome_dataframe = self.outcome_specific_dataframes.negative_outcome_dataframe[list_of_columns]
        positive_outcome_dataframe = self.outcome_specific_dataframes.positive_outcome_dataframe[list_of_columns]

        for column in list_of_columns:
            negative_outcome_dataframe = self.get_dataframe_with_strings_converted_to_nan_in_given_column(
                column_name=column,
                dataframe=negative_outcome_dataframe
            )
            positive_outcome_dataframe = self.get_dataframe_with_strings_converted_to_nan_in_given_column(
                column_name=column,
                dataframe=positive_outcome_dataframe
            )

        outcome_specific_dataframes = self.OutcomeDataFrames(
            negative_outcome_dataframe=negative_outcome_dataframe,
            positive_outcome_dataframe=positive_outcome_dataframe,
        )

        return outcome_specific_dataframes

    def get_descriptive_stats_dataframe_from_given_columns(self, list_of_columns: list) -> pd.DataFrame:
        reduced_dataset = self.dataframe[list_of_columns]
        descriptive_stats_dataframe = reduced_dataset.describe().transpose().round(decimals=1)

        return descriptive_stats_dataframe

    def get_frequency_table(self, list_of_columns: list):
        dataframe = pd.DataFrame(columns=["Variable", "Level", "n", "%"])

        number_of_levels = 0
        for variable_idx, variable_name in enumerate(list_of_columns):
            value_counts: pd.Series = self.dataframe[variable_name].value_counts()
            ratio_counts: pd.Series = self.dataframe[variable_name].value_counts(normalize=True)

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

    def get_frequency_table_and_test_on_proportions(self, list_of_columns: list, outcome: str):
        dataframe = pd.DataFrame(columns=["Variable", "Level", "n/N", "%", "n/N", "%", "p-value"])
        self.outcome = outcome

        negative_outcome_dataframe = self.outcome_specific_dataframes.negative_outcome_dataframe
        positive_outcome_dataframe = self.outcome_specific_dataframes.positive_outcome_dataframe

        number_of_levels = 0
        for variable_idx, variable_name in enumerate(list_of_columns):
            value_counts_pn0: pd.Series = negative_outcome_dataframe[variable_name].value_counts()
            ratio_counts_pn0: pd.Series = negative_outcome_dataframe[variable_name].value_counts(normalize=True)

            levels_pn0 = list(value_counts_pn0.index)
            counts_pn0 = value_counts_pn0.to_list()
            percentage_counts_pn0 = round(ratio_counts_pn0 * 100, ndigits=1).to_list()

            value_counts_pn1: pd.Series = positive_outcome_dataframe[variable_name].value_counts()
            ratio_counts_pn1: pd.Series = positive_outcome_dataframe[variable_name].value_counts(normalize=True)

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

    def pN_frequency_table(self, column_name: str):
        result = pd.concat(
            [
                self.outcome_specific_dataframes.negative_outcome_dataframe[column_name].value_counts(),
                self.outcome_specific_dataframes.positive_outcome_dataframe[column_name].value_counts()
            ],
            axis=1
        )
        result = result.fillna(0)

        return result

    def chi2_test_on_frequency_table(self, column_name: str):
        result = self.pN_frequency_table(column_name=column_name)
        chi2, p_value, dof, expected = stats.chi2_contingency(observed=result)

        return p_value

    def mann_whitney_u_test(
            self,
            column_name: str,
            negative_outcome_dataframe: pd.DataFrame,
            positive_outcome_dataframe: pd.DataFrame
    ):
        _, p = stats.mannwhitneyu(
            x=negative_outcome_dataframe[column_name].dropna(),
            y=positive_outcome_dataframe[column_name].dropna()
        )

        return p

    def get_descriptive_stats_dataframe_from_pn(self, list_of_columns: list, outcome: str) -> pd.DataFrame:
        outcome_specific_dataframes = self.get_dataframes_subset_from_given_columns(
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
                p_value = self.mann_whitney_u_test(
                    column_name=label,
                    negative_outcome_dataframe=negative_outcome_dataframe,
                    positive_outcome_dataframe=positive_outcome_dataframe
                )

            p_values.append(p_value)

        concat_df["p-value"] = p_values

        return concat_df
