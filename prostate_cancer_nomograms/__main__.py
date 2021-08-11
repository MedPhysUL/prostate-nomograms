import logging
from root import *
from logging_tools import logs_file_setup
import pandas as pd
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
    dataset_name = "mock_dataset.xlsx"
    results_name = "mock_results_dataset.csv"

    number_of_years = 5

    post_radical_prostatectomy_model_name = f"Postoperative BCR"
    pre_radical_prostatectomy_model_name = f"Preoperative BCR (Cores)"

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Data                                                       #
    # ----------------------------------------------------------------------------------------------------------- #
    patient_dataframe: pd.DataFrame = pd.read_excel(os.path.join(PATH_TO_DATA_FOLDER, dataset_name))

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Post Radical Prostatectomy                                         #
    # ----------------------------------------------------------------------------------------------------------- #
    post_radical_prostatectomy_model = PostRadicalProstatectomyModel(
        patients_dataframe=patient_dataframe,
        model_name=post_radical_prostatectomy_model_name
    )

    # ----------------------------------------------------------------------------------------------------------- #
    #                                    MSKCC Pre Radical Prostatectomy                                          #
    # ----------------------------------------------------------------------------------------------------------- #
    pre_radical_prostatectomy_model = PreRadicalProstatectomyModel(
        patients_dataframe=patient_dataframe,
        model_name=pre_radical_prostatectomy_model_name
    )

    # ----------------------------------------------------------------------------------------------------------- #
    #                                                  Results                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    post_column_name = f"{post_radical_prostatectomy_model_name}_{number_of_years}_years"
    pre_column_name = f"{pre_radical_prostatectomy_model_name}_{number_of_years}_years"

    patient_dataframe[post_column_name] = post_radical_prostatectomy_model.get_predictions(
        number_of_years=number_of_years
    )
    patient_dataframe[pre_column_name] = pre_radical_prostatectomy_model.get_predictions(
        number_of_years=number_of_years
    )

    patient_dataframe.to_csv(path_or_buf=os.path.join(PATH_TO_RESULTS_FOLDER, results_name))
