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
    dataset_name = "Data_preop.xlsx"
    results_name = "Results_preop.csv"

    numbers_of_years = [5, 10]
    clean_dataframe = True

    post_radical_prostatectomy_model_names = ["Postoperative BCR"]
    pre_radical_prostatectomy_model_names = ["Preoperative BCR (Cores)", "Lymph Node Involvement (Cores)"]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Data                                                       #
    # ----------------------------------------------------------------------------------------------------------- #
    patient_dataframe: pd.DataFrame = pd.read_excel(os.path.join(PATH_TO_DATA_FOLDER, dataset_name))

    if clean_dataframe:
        patient_dataframe.dropna(subset=["Stade clinique"], inplace=True)
        patient_dataframe = patient_dataframe[patient_dataframe["Stade clinique"] != "n/d"]
        patient_dataframe = patient_dataframe[patient_dataframe["NbCtePositive"] != "N.D."]
        patient_dataframe = patient_dataframe[patient_dataframe["NbCteNegative"] != "N.D."]

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                   CAPRA                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    capra = CAPRA(patients_dataframe=patient_dataframe)
    capra.show_histogram()
    patient_dataframe["CAPRA Score"] = capra.get_capra_score()

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Post Radical Prostatectomy                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    # post_radical_prostatectomy_model = PostRadicalProstatectomyModel(
    #     patients_dataframe=patient_dataframe,
    #     model_name=post_radical_prostatectomy_model_name
    # )
    # post_column_name = f"{post_radical_prostatectomy_model_name}_{number_of_years}_years"
    # patient_dataframe[post_column_name] = post_radical_prostatectomy_model.get_predictions(
    #     number_of_years=number_of_years
    # )

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Pre Radical Prostatectomy                                          #
    # ----------------------------------------------------------------------------------------------------------- #
    # for pre_radical_prostatectomy_model_name in pre_radical_prostatectomy_model_names:
    #     pre_radical_prostatectomy_model = PreRadicalProstatectomyModel(
    #         patients_dataframe=patient_dataframe,
    #         model_name=pre_radical_prostatectomy_model_name
    #     )
    #
    #     if pre_radical_prostatectomy_model_name == "Preoperative BCR (Cores)":
    #
    #         for number_of_years in numbers_of_years:
    #
    #             pre_column_name = f"{pre_radical_prostatectomy_model_name}_{number_of_years}_years"
    #
    #             patient_dataframe[pre_column_name] = pre_radical_prostatectomy_model.get_predictions(
    #                 number_of_years=number_of_years
    #             )
    #     else:
    #         pre_column_name = f"{pre_radical_prostatectomy_model_name}"
    #
    #         patient_dataframe[pre_column_name] = pre_radical_prostatectomy_model.get_predictions()

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    patient_dataframe.to_csv(path_or_buf=os.path.join(PATH_TO_DATA_FOLDER, results_name))
