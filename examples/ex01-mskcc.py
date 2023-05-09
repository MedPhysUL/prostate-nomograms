import env_examples

import os

import pandas as pd

from src.nomograms import MSKCCPreRadicalProstatectomyModel, Outcome


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATA_FOLDER_NAME = "data"
    DATASET_FILENAME = "fake_dataset.xlsx"
    RESULTS_FILENAME = "results.csv"
    DATASET_PATH = os.path.join(DATA_FOLDER_NAME, DATASET_FILENAME)
    RESULTS_PATH = os.path.join(DATA_FOLDER_NAME, RESULTS_FILENAME)

    MSKCC_EXCLUDED_COLUMN = "MSKCC_EXCLUDED"
    CAPRA_SCORE_COLUMN = "CAPRA_SCORE"
    AGE_COLUMN = "AGE"
    PSA_COLUMN = "PSA"
    CLINICAL_STAGE_COLUMN = "CLINICAL_STAGE"
    GLEASON_PRIMARY_COLUMN = "GLEASON_PRIMARY"
    GLEASON_SECONDARY_COLUMN = "GLEASON_SECONDARY"

    NUMBER_OF_YEARS = [5, 10]

    OUTCOMES = [
        Outcome.PREOPERATIVE_BCR,
        Outcome.EXTRACAPSULAR_EXTENSION,
        Outcome.LYMPH_NODE_INVOLVEMENT,
        Outcome.ORGAN_CONFINED_DISEASE,
        Outcome.SEMINAL_VESICLE_INVASION,
        # Outcome.PREOPERATIVE_PROSTATE_CANCER_DEATH
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
        mskcc_model = MSKCCPreRadicalProstatectomyModel(outcome=outcome)
        if outcome in SURVIVAL_OUTCOMES:
            for number_of_years in NUMBER_OF_YEARS:
                column_name = f"{outcome}_{number_of_years}_years"
                dataframe[column_name] = mskcc_model.predict_proba(dataframe, number_of_years)
        else:
            dataframe[outcome] = mskcc_model.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
