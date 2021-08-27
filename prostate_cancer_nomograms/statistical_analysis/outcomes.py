import enum
from typing import Any, NamedTuple


class OutcomeDataFrameInformation(NamedTuple):
    column_name_in_dataframe: str
    value_of_negative_outcome: Any
    value_of_positive_outcome: Any


LYMPH_NODE_INFO = OutcomeDataFrameInformation(
    column_name_in_dataframe="pN",
    value_of_negative_outcome="pN0",
    value_of_positive_outcome="pN1"
)

BCR_5YEARS_INFO = OutcomeDataFrameInformation(
    column_name_in_dataframe="Récurrence 5 ans (60 mois), oui = 1; non =0",
    value_of_negative_outcome=0,
    value_of_positive_outcome=1
)


class Outcomes(enum.Enum):
    LYMPH_NODE = LYMPH_NODE_INFO
    BCR_5YEARS = BCR_5YEARS_INFO
