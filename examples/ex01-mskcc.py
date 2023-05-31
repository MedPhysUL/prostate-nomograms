import env_examples

import os

import pandas as pd

from nomograms import MSKCCPreRadicalProstatectomyNomogram, Outcome


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATA_FOLDER_NAME = "data"
    DATASET_FILENAME = "fake_dataset.xlsx"
    RESULTS_FILENAME = "mskcc_results.csv"
    DATASET_PATH = os.path.join(DATA_FOLDER_NAME, DATASET_FILENAME)
    RESULTS_PATH = os.path.join(DATA_FOLDER_NAME, RESULTS_FILENAME)

    MSKCC_EXCLUDED_COLUMN = "MSKCC_EXCLUDED"
    CAPRA_SCORE_COLUMN = "CAPRA_SCORE"
    AGE_COLUMN = "AGE"
    PSA_COLUMN = "PSA"
    CLINICAL_STAGE_COLUMN = "CLINICAL_STAGE_MSKCC"
    GLEASON_PRIMARY_COLUMN = "GLEASON_PRIMARY"
    GLEASON_SECONDARY_COLUMN = "GLEASON_SECONDARY"

    NUMBER_OF_MONTHS = [60, 120, 180]

    OUTCOMES = [
        Outcome.PREOPERATIVE_BCR,
        Outcome.EXTRACAPSULAR_EXTENSION,
        Outcome.LYMPH_NODE_INVOLVEMENT,
        Outcome.SEMINAL_VESICLE_INVASION,
        Outcome.ORGAN_CONFINED_DISEASE,
        Outcome.PREOPERATIVE_PROSTATE_CANCER_DEATH
    ]

    SURVIVAL_OUTCOMES = [
        Outcome.PREOPERATIVE_BCR,
        Outcome.PREOPERATIVE_PROSTATE_CANCER_DEATH
    ]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                    Data                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe = pd.read_excel(DATASET_PATH)
    dataframe = dataframe[dataframe[MSKCC_EXCLUDED_COLUMN] == 0]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                   MSKCC                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    for outcome in OUTCOMES:
        mskcc_model = MSKCCPreRadicalProstatectomyNomogram(
            outcome=outcome,
            age_column_name=AGE_COLUMN,
            psa_column_name=PSA_COLUMN,
            primary_gleason_column_name=GLEASON_PRIMARY_COLUMN,
            secondary_gleason_column_name=GLEASON_SECONDARY_COLUMN,
            clinical_stage_column_name=CLINICAL_STAGE_COLUMN
        )
        if outcome in SURVIVAL_OUTCOMES:
            dataframe[f"{outcome}_risk"] = mskcc_model.predict_risk(dataframe)
            for number_of_months in NUMBER_OF_MONTHS:
                column_name = f"{outcome}_{number_of_months}_months"
                dataframe[column_name] = mskcc_model.predict_proba(dataframe, number_of_months)
        else:
            dataframe[outcome] = mskcc_model.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
