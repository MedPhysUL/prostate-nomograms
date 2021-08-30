import logging
from copy import deepcopy
from root import *
from logging_tools import logs_file_setup
import pandas as pd
from CAPRA.capra import CAPRA
from MSKCC.pre_radical_prostatectomy.pre_radical_prostatectomy_model import PreRadicalProstatectomyModel

if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                          Logs Setup                                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(__file__, logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATASET_NAME = "fake_dataset.xlsx"
    RESULTS_NAME_CORES_DEPENDANT = "CORES_DEPENDANT_results.csv"

    NUMBER_OF_YEARS = [5, 10]
    CLEAN_DATAFRAME = True

    POST_RADICAL_PROSTATECTOMY_MODEL_NAME = "Postoperative BCR"

    PRE_RADICAL_PROSTATECTOMY_MODEL_NAMES = [
        "Preoperative BCR (Cores)",
        "Extracapsular Extension (Cores)",
        "Lymph Node Involvement (Cores)",
        "Organ Confined Disease (Cores)",
        "Seminal Vesicle Invasion (Cores)",
    ]

    PRE_RADICAL_PROSTATECTOMY_CORES_FREE_MODEL_NAMES = [
        "Preoperative BCR",
        "Extracapsular Extension",
        "Lymph Node Involvement",
        "Organ Confined Disease",
        "Seminal Vesicle Invasion",
    ]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Data                                                       #
    # ----------------------------------------------------------------------------------------------------------- #
    patient_dataframe: pd.DataFrame = pd.read_excel(os.path.join(PATH_TO_DATA_FOLDER, DATASET_NAME))

    mskcc_allowed_patient_dataframe = deepcopy(patient_dataframe[patient_dataframe["À exclure du MSKCC (oui =1, non=0)"] == 0])
    mskcc_allowed_clean_cores_patient_dataframe = deepcopy(
        patient_dataframe[
            patient_dataframe["À exclure du MSKCC (oui =1, non=0)"] == 0
            ]
    )

    # ----------------------------------------------------------------------------------------------------------- #
    #                                     CAPRA with MSKCC restrictions                                           #
    # ----------------------------------------------------------------------------------------------------------- #
    capra = CAPRA(patients_dataframe=mskcc_allowed_clean_cores_patient_dataframe)
    mskcc_allowed_clean_cores_patient_dataframe["CAPRA Score"] = capra.get_capra_score()

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Pre Radical Prostatectomy                                          #
    # ----------------------------------------------------------------------------------------------------------- #
    for pre_radical_prostatectomy_model_name in PRE_RADICAL_PROSTATECTOMY_MODEL_NAMES:
        pre_radical_prostatectomy_model = PreRadicalProstatectomyModel(
            patients_dataframe=mskcc_allowed_clean_cores_patient_dataframe,
            model_name=pre_radical_prostatectomy_model_name
        )

        if pre_radical_prostatectomy_model_name == "Preoperative BCR (Cores)":

            for number_of_years in NUMBER_OF_YEARS:

                column_name = f"{pre_radical_prostatectomy_model_name}_{number_of_years}_years"

                mskcc_allowed_clean_cores_patient_dataframe[column_name] = pre_radical_prostatectomy_model.get_predictions(
                    number_of_years=number_of_years
                )
        else:
            column_name = f"{pre_radical_prostatectomy_model_name}"

            mskcc_allowed_clean_cores_patient_dataframe[column_name] = pre_radical_prostatectomy_model.get_predictions()

    for pre_radical_prostatectomy_cores_free_model_name in PRE_RADICAL_PROSTATECTOMY_CORES_FREE_MODEL_NAMES:
        pre_radical_prostatectomy_cores_free_model = PreRadicalProstatectomyModel(
            patients_dataframe=mskcc_allowed_patient_dataframe,
            model_name=pre_radical_prostatectomy_cores_free_model_name
        )

        if pre_radical_prostatectomy_cores_free_model_name == "Preoperative BCR":

            for number_of_years in NUMBER_OF_YEARS:

                column_name = f"{pre_radical_prostatectomy_cores_free_model_name}_{number_of_years}_years"

                mskcc_allowed_patient_dataframe[column_name] = pre_radical_prostatectomy_cores_free_model.get_predictions(
                    number_of_years=number_of_years
                )
        else:
            column_name = f"{pre_radical_prostatectomy_cores_free_model_name}"

            mskcc_allowed_patient_dataframe[column_name] = pre_radical_prostatectomy_cores_free_model.get_predictions()

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    mskcc_allowed_clean_cores_patient_dataframe.to_csv(
        path_or_buf=os.path.join(PATH_TO_DATA_FOLDER, RESULTS_NAME_CORES_DEPENDANT)
    )

