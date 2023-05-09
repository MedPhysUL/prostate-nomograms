import env_examples

import os

import pandas as pd

from src.nomograms import CAPRAModel, Outcome


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

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                   CAPRA                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    capra_model = CAPRAModel(
        outcome=Outcome.LYMPH_NODE_INVOLVEMENT,
        target_column_name="pN",
        age_column_name=AGE_COLUMN,
        psa_column_name=PSA_COLUMN,
        clinical_stage_column_name=CLINICAL_STAGE_COLUMN,
        primary_gleason_column_name=GLEASON_PRIMARY_COLUMN,
        secondary_gleason_column_name=GLEASON_SECONDARY_COLUMN
    )
    dataframe[CAPRA_SCORE_COLUMN] = capra_model.get_capra_score(dataframe)

    # for outcome in OUTCOMES:
    #     if outcome in SURVIVAL_OUTCOMES:
    #         capra_model = CAPRAModel(
    #             outcome=outcome,
    #             event_indicator_column_name=,
    #             event_time_column_name=
    #         )
    #         capra_model.fit(dataframe)
    #         for number_of_years in NUMBER_OF_YEARS:
    #             column_name = f"{outcome}_{number_of_years}_years"
    #             dataframe[column_name] = capra_model.predict_proba(dataframe, number_of_years)
    #     else:
    #         capra_model = CAPRAModel(
    #             outcome=outcome,
    #             target_column_name=
    #         )
    #         capra_model.fit(dataframe)
    #         dataframe[outcome] = capra_model.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
