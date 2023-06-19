import env_examples

import os

import pandas as pd

from prostate_nomograms import CustomNomogram, ClassificationOutcome, SurvivalOutcome


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATA_FOLDER_NAME = "data"
    DATASET_FILENAME = "fake_dataset_numerical.xlsx"
    RESULTS_FILENAME = "results_custom.csv"
    DATASET_PATH = os.path.join(DATA_FOLDER_NAME, DATASET_FILENAME)
    RESULTS_PATH = os.path.join(DATA_FOLDER_NAME, RESULTS_FILENAME)

    AGE_COLUMN = "AGE"
    PSA_COLUMN = "PSA"
    CLINICAL_STAGE_COLUMN = "CLINICAL_STAGE"
    GLEASON_PRIMARY_COLUMN = "GLEASON_PRIMARY"
    GLEASON_SECONDARY_COLUMN = "GLEASON_SECONDARY"
    GLEASON_GLOBAL_COLUMN = "GLEASON_GLOBAL"

    NUMBER_OF_MONTHS = [60, 120]

    OUTCOMES = {
        ClassificationOutcome.EXTRACAPSULAR_EXTENSION: "EE",
        ClassificationOutcome.LYMPH_NODE_INVOLVEMENT: "PN",
        ClassificationOutcome.SEMINAL_VESICLE_INVASION: "SVI",
        ClassificationOutcome.ORGAN_CONFINED_DISEASE: "OCD",
        SurvivalOutcome.PREOPERATIVE_BCR: "BCR",
        SurvivalOutcome.PREOPERATIVE_PROSTATE_CANCER_DEATH: "DEATH"
    }

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                    Data                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe = pd.read_excel(DATASET_PATH)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                   Custom                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    for outcome, col_name in OUTCOMES.items():
        if outcome in SurvivalOutcome:
            custom_nomogram = CustomNomogram(
                outcome=outcome,
                event_indicator_column_name=col_name,
                event_time_column_name=f"{col_name}_TIME",
                features_column_names=[
                    AGE_COLUMN,
                    PSA_COLUMN,
                    GLEASON_PRIMARY_COLUMN,
                    GLEASON_SECONDARY_COLUMN,
                    GLEASON_GLOBAL_COLUMN,
                    CLINICAL_STAGE_COLUMN
                ]
            )
            custom_nomogram.fit(dataframe)
            dataframe[f"PREDICTED_{outcome.name}_RISK"] = custom_nomogram.predict_risk(dataframe)
            for number_of_months in NUMBER_OF_MONTHS:
                column_name = f"PREDICTED_{outcome.name}_{number_of_months}MONTHS"
                dataframe[column_name] = custom_nomogram.predict_proba(dataframe, number_of_months)
        else:
            custom_nomogram = CustomNomogram(
                outcome=outcome,
                target_column_name=col_name,
                features_column_names=[
                    AGE_COLUMN,
                    PSA_COLUMN,
                    GLEASON_PRIMARY_COLUMN,
                    GLEASON_SECONDARY_COLUMN,
                    GLEASON_GLOBAL_COLUMN,
                    CLINICAL_STAGE_COLUMN
                ]
            )
            custom_nomogram.fit(dataframe)
            dataframe[f"PREDICTED_{outcome.name}"] = custom_nomogram.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
