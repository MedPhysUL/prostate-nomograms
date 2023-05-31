import env_examples

import os

import pandas as pd

from nomograms import CAPRANomogram, Outcome


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATA_FOLDER_NAME = "data"
    DATASET_FILENAME = "fake_dataset.xlsx"
    RESULTS_FILENAME = "capra_results.csv"
    DATASET_PATH = os.path.join(DATA_FOLDER_NAME, DATASET_FILENAME)
    RESULTS_PATH = os.path.join(DATA_FOLDER_NAME, RESULTS_FILENAME)

    CAPRA_SCORE_COLUMN = "CAPRA_SCORE"
    AGE_COLUMN = "AGE"
    PSA_COLUMN = "PSA"
    CLINICAL_STAGE_COLUMN = "CLINICAL_STAGE"
    GLEASON_PRIMARY_COLUMN = "GLEASON_PRIMARY"
    GLEASON_SECONDARY_COLUMN = "GLEASON_SECONDARY"

    NUMBER_OF_MONTHS = [60, 120]

    OUTCOMES = {
        Outcome.PREOPERATIVE_BCR: "BCR",
        Outcome.EXTRACAPSULAR_EXTENSION: "EE",
        Outcome.LYMPH_NODE_INVOLVEMENT: "PN",
        Outcome.SEMINAL_VESICLE_INVASION: "SVI",
        Outcome.ORGAN_CONFINED_DISEASE: "OCD",
        Outcome.PREOPERATIVE_PROSTATE_CANCER_DEATH: "DEATH"
    }

    SURVIVAL_OUTCOMES = [
        Outcome.PREOPERATIVE_BCR,
        Outcome.PREOPERATIVE_PROSTATE_CANCER_DEATH
    ]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                    Data                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe = pd.read_excel(DATASET_PATH)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                   CAPRA                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    for outcome, col_name in OUTCOMES.items():
        if outcome in SURVIVAL_OUTCOMES:
            capra_model = CAPRANomogram(
                outcome=outcome,
                event_indicator_column_name=col_name,
                event_time_column_name=f"{col_name}_TIME",
                age_column_name=AGE_COLUMN,
                psa_column_name=PSA_COLUMN,
                primary_gleason_column_name=GLEASON_PRIMARY_COLUMN,
                secondary_gleason_column_name=GLEASON_SECONDARY_COLUMN,
                clinical_stage_column_name=CLINICAL_STAGE_COLUMN
            )
            capra_model.fit(dataframe)
            dataframe[f"{outcome}_risk"] = capra_model.predict_risk(dataframe)
            for number_of_months in NUMBER_OF_MONTHS:
                column_name = f"{outcome}_{number_of_months}_months"
                dataframe[column_name] = capra_model.predict_proba(dataframe, number_of_months)
        else:
            capra_model = CAPRANomogram(
                outcome=outcome,
                target_column_name=col_name
            )
            capra_model.fit(dataframe)
            dataframe[outcome] = capra_model.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
