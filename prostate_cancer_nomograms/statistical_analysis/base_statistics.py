from typing import NamedTuple
import pandas as pd
from .outcomes import Outcomes, OutcomeDataFrameInformation


class BaseStatistics:

    class OutcomeDataFrames(NamedTuple):
        negative_outcome_dataframe: pd.DataFrame
        positive_outcome_dataframe: pd.DataFrame

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self._outcome = None

    @property
    def outcome(self) -> str:
        return self._outcome

    @outcome.setter
    def outcome(self, outcome: str):
        if outcome in Outcomes.__members__:
            self._outcome = outcome
        else:
            raise ValueError(f"Given member {outcome} is not allowed. Allowed members of {Outcomes} are "
                             f"{list(Outcomes.__members__)}.")

    @property
    def outcome_specific_dataframes_information(self) -> OutcomeDataFrameInformation:
        return Outcomes[self.outcome].value

    @property
    def outcome_specific_dataframes(self) -> OutcomeDataFrames:
        column_name = self.outcome_specific_dataframes_information.outcome_column_name_in_dataframe
        value_of_negative_outcome = self.outcome_specific_dataframes_information.value_of_negative_outcome
        value_of_positive_outcome = self.outcome_specific_dataframes_information.value_of_positive_outcome

        outcome_specific_dataframes = self.OutcomeDataFrames(
            negative_outcome_dataframe=self.dataframe[self.dataframe[column_name] == value_of_negative_outcome],
            positive_outcome_dataframe=self.dataframe[self.dataframe[column_name] == value_of_positive_outcome],
        )

        return outcome_specific_dataframes

    @property
    def negative_outcome_dataframe(self) -> pd.DataFrame:
        return self.outcome_specific_dataframes.negative_outcome_dataframe

    @property
    def positive_outcome_dataframe(self) -> pd.DataFrame:
        return self.outcome_specific_dataframes.positive_outcome_dataframe
