import logging
from root import *
from logging_tools import logs_file_setup
import pandas as pd
from CAPRA.capra import CAPRA
from MSKCC.post_radical_prostatectomy.post_radical_prostatectomy_model import PostRadicalProstatectomyModel
from MSKCC.pre_radical_prostatectomy.pre_radical_prostatectomy_model import PreRadicalProstatectomyModel

if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                          Logs Setup                                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(__file__, logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                Constant                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    DATASET_NAME = "Data_preop.xlsx"
    RESULTS_NAME_CORES_DEPENDANT = "Cores_dependent_results.csv"
    RESULTS_NAME_CORES_INDEPENDENT = "Cores_independent_results.csv"

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

    if CLEAN_DATAFRAME:
        patient_dataframe.dropna(subset=["Stade clinique"], inplace=True)
        patient_dataframe = patient_dataframe[patient_dataframe["Stade clinique"] != "n/d"]

    clean_cores_patient_dataframe = patient_dataframe[patient_dataframe["NbCtePositive"] != "N.D."]
    clean_cores_patient_dataframe = \
        clean_cores_patient_dataframe[clean_cores_patient_dataframe["NbCteNegative"] != "N.D."]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                   CAPRA                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    capra = CAPRA(patients_dataframe=clean_cores_patient_dataframe)
    clean_cores_patient_dataframe["CAPRA Score"] = capra.get_capra_score()

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Post Radical Prostatectomy                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    # for number_of_years in NUMBER_OF_YEARS:
    #     post_radical_prostatectomy_model = PostRadicalProstatectomyModel(
    #         patients_dataframe=patient_dataframe,
    #         model_name=POST_RADICAL_PROSTATECTOMY_MODEL_NAME
    #     )
    #
    #     post_column_name = f"{POST_RADICAL_PROSTATECTOMY_MODEL_NAME}_{number_of_years}_years"
    #
    #     patient_dataframe[post_column_name] = post_radical_prostatectomy_model.get_predictions(
    #         number_of_years=number_of_years
    #     )

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Pre Radical Prostatectomy                                          #
    # ----------------------------------------------------------------------------------------------------------- #
    for pre_radical_prostatectomy_model_name in PRE_RADICAL_PROSTATECTOMY_MODEL_NAMES:
        pre_radical_prostatectomy_model = PreRadicalProstatectomyModel(
            patients_dataframe=clean_cores_patient_dataframe,
            model_name=pre_radical_prostatectomy_model_name
        )

        if pre_radical_prostatectomy_model_name == "Preoperative BCR (Cores)":

            for number_of_years in NUMBER_OF_YEARS:

                column_name = f"{pre_radical_prostatectomy_model_name}_{number_of_years}_years"

                clean_cores_patient_dataframe[column_name] = pre_radical_prostatectomy_model.get_predictions(
                    number_of_years=number_of_years
                )
        else:
            column_name = f"{pre_radical_prostatectomy_model_name}"

            clean_cores_patient_dataframe[column_name] = pre_radical_prostatectomy_model.get_predictions()

    for pre_radical_prostatectomy_cores_free_model_name in PRE_RADICAL_PROSTATECTOMY_CORES_FREE_MODEL_NAMES:
        pre_radical_prostatectomy_cores_free_model = PreRadicalProstatectomyModel(
            patients_dataframe=patient_dataframe,
            model_name=pre_radical_prostatectomy_cores_free_model_name
        )

        if pre_radical_prostatectomy_cores_free_model_name == "Preoperative BCR":

            for number_of_years in NUMBER_OF_YEARS:

                column_name = f"{pre_radical_prostatectomy_cores_free_model_name}_{number_of_years}_years"

                patient_dataframe[column_name] = pre_radical_prostatectomy_cores_free_model.get_predictions(
                    number_of_years=number_of_years
                )
        else:
            column_name = f"{pre_radical_prostatectomy_cores_free_model_name}"

            patient_dataframe[column_name] = pre_radical_prostatectomy_cores_free_model.get_predictions()

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    patient_dataframe.to_csv(path_or_buf=os.path.join(PATH_TO_DATA_FOLDER, RESULTS_NAME_CORES_INDEPENDENT))
    clean_cores_patient_dataframe.to_csv(path_or_buf=os.path.join(PATH_TO_DATA_FOLDER, RESULTS_NAME_CORES_DEPENDANT))
