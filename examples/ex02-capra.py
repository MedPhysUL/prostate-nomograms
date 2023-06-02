import env_examples

import os

import pandas as pd

from prostate_nomograms import CapraNomogram, ClassificationOutcome, SurvivalOutcome


if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATA_FOLDER_NAME = "data"
    DATASET_FILENAME = "fake_dataset.xlsx"
    RESULTS_FILENAME = "results_capra.csv"
    DATASET_PATH = os.path.join(DATA_FOLDER_NAME, DATASET_FILENAME)
    RESULTS_PATH = os.path.join(DATA_FOLDER_NAME, RESULTS_FILENAME)

    AGE_COLUMN = "AGE"
    PSA_COLUMN = "PSA"
    CLINICAL_STAGE_COLUMN = "CLINICAL_STAGE"
    GLEASON_PRIMARY_COLUMN = "GLEASON_PRIMARY"
    GLEASON_SECONDARY_COLUMN = "GLEASON_SECONDARY"

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
    #                                                   CAPRA                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    for outcome, col_name in OUTCOMES.items():
        if outcome in SurvivalOutcome:
            capra_nomogram = CapraNomogram(
                outcome=outcome,
                event_indicator_column_name=col_name,
                event_time_column_name=f"{col_name}_TIME",
                age_column_name=AGE_COLUMN,
                psa_column_name=PSA_COLUMN,
                primary_gleason_column_name=GLEASON_PRIMARY_COLUMN,
                secondary_gleason_column_name=GLEASON_SECONDARY_COLUMN,
                clinical_stage_column_name=CLINICAL_STAGE_COLUMN
            )
            capra_nomogram.fit(dataframe)
            dataframe[f"PREDICTED_{outcome.name}_RISK"] = capra_nomogram.predict_risk(dataframe)
            for number_of_months in NUMBER_OF_MONTHS:
                column_name = f"PREDICTED_{outcome.name}_{number_of_months}MONTHS"
                dataframe[column_name] = capra_nomogram.predict_proba(dataframe, number_of_months)
        else:
            capra_nomogram = CapraNomogram(outcome=outcome, target_column_name=col_name)
            capra_nomogram.fit(dataframe)
            dataframe[f"PREDICTED_{outcome.name}"] = capra_nomogram.predict_proba(dataframe)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataframe.to_csv(path_or_buf=RESULTS_PATH)
