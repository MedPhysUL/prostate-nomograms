import enum
from typing import Any, NamedTuple


class OutcomeDataFrameInformation(NamedTuple):
    outcome_column_name_in_dataframe: str
    probability_column_name_in_dataframe: str
    value_of_negative_outcome: Any
    value_of_positive_outcome: Any


LYMPH_NODE_INFO = OutcomeDataFrameInformation(
    outcome_column_name_in_dataframe="pN",
    probability_column_name_in_dataframe="Lymph Node Involvement (Cores)",
    value_of_negative_outcome="pN0",
    value_of_positive_outcome="pN1"
)

BCR_5YEARS_INFO = OutcomeDataFrameInformation(
    outcome_column_name_in_dataframe="Récurrence 5 ans (60 mois), oui = 1; non =0",
    probability_column_name_in_dataframe="Preoperative BCR (Cores)_5_years",
    value_of_negative_outcome=1,
    value_of_positive_outcome=0
)


class Outcomes(enum.Enum):
    LYMPH_NODE = LYMPH_NODE_INFO
    BCR_5YEARS = BCR_5YEARS_INFO
