import env_examples

import os

import pandas as pd

from prostate_nomograms import MskccPreRadicalProstatectomyNomogram, ClassificationOutcome, SurvivalOutcome


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATA_FOLDER_NAME = "data"
    DATASET_FILENAME = "fake_dataset.xlsx"
    RESULTS_FILENAME = "results_mskcc.csv"
    DATASET_PATH = os.path.join(DATA_FOLDER_NAME, DATASET_FILENAME)
    RESULTS_PATH = os.path.join(DATA_FOLDER_NAME, RESULTS_FILENAME)

    MSKCC_EXCLUDED_COLUMN = "MSKCC_EXCLUDED"
    AGE_COLUMN = "AGE"
    PSA_COLUMN = "PSA"
    CLINICAL_STAGE_COLUMN = "CLINICAL_STAGE_MSKCC"
    GLEASON_PRIMARY_COLUMN = "GLEASON_PRIMARY"
    GLEASON_SECONDARY_COLUMN = "GLEASON_SECONDARY"

    NUMBER_OF_MONTHS = [60, 120, 180]

    OUTCOMES = [
        ClassificationOutcome.EXTRACAPSULAR_EXTENSION,
        ClassificationOutcome.LYMPH_NODE_INVOLVEMENT,
        ClassificationOutcome.SEMINAL_VESICLE_INVASION,
        ClassificationOutcome.ORGAN_CONFINED_DISEASE,
        SurvivalOutcome.PREOPERATIVE_BCR,
        SurvivalOutcome.PREOPERATIVE_PROSTATE_CANCER_DEATH
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
        mskcc_nomogram = MskccPreRadicalProstatectomyNomogram(
            outcome=outcome,
            age_column_name=AGE_COLUMN,
            psa_column_name=PSA_COLUMN,
            primary_gleason_column_name=GLEASON_PRIMARY_COLUMN,
            secondary_gleason_column_name=GLEASON_SECONDARY_COLUMN,
            clinical_stage_column_name=CLINICAL_STAGE_COLUMN
        )

        if outcome in SurvivalOutcome:
            dataframe[f"PREDICTED_{outcome.name}_RISK"] = mskcc_nomogram.predict_risk(dataframe)
            for number_of_months in NUMBER_OF_MONTHS:
                column_name = f"PREDICTED_{outcome.name}_{number_of_months}MONTHS"
                dataframe[column_name] = mskcc_nomogram.predict_proba(dataframe, number_of_months)
        else:
            dataframe[f"PREDICTED_{outcome.name}"] = mskcc_nomogram.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
