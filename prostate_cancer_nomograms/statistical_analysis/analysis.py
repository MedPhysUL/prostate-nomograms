import os
import logging

from prostate_cancer_nomograms.logging_tools import logs_file_setup, section_title_log, sub_section_title_log
from prostate_cancer_nomograms.statistical_analysis.outcomes import Outcomes
from prostate_cancer_nomograms.root import PATH_TO_DATA_FOLDER
from prostate_cancer_nomograms.statistical_analysis.dataset_loader import DatasetLoader
from prostate_cancer_nomograms.statistical_analysis.descriptive_statistics import DescriptiveStatistics

if __name__ == "__main__":
    # ----------------------------------------------------------------------------------------------------------- #
    #                                              Logs Setup                                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    logs_file_setup(__file__, logging.INFO)

    # ----------------------------------------------------------------------------------------------------------- #
    #                                             Data Loading                                                    #
    # ----------------------------------------------------------------------------------------------------------- #
    dataset_loader = DatasetLoader(path_to_dataset=os.path.join(PATH_TO_DATA_FOLDER, "PreOp_Cores_dependent_results.csv"))
    dataset = dataset_loader.dataset

    # ----------------------------------------------------------------------------------------------------------- #
    #                                         Descriptive statistics                                              #
    # ----------------------------------------------------------------------------------------------------------- #
    section_title_log(section_title="Descriptive statistics")

    descriptive_statistics = DescriptiveStatistics(dataframe=dataset)

    # -------- General Statistics -------- #
    list_of_columns = [
        "Âge au diagnostique",
        "PSA au diagnostique",
        "% cores POS",
        "% cores NEG",
        "PSA_valeur de récidive",
        "Durée de suivi (mois)",
        "Dernière PSA",
        "pN"
    ]
    descriptive_stats_table = descriptive_statistics.get_descriptive_stats_dataframe_from_given_columns(
        list_of_columns=list_of_columns
    )
    sub_section_title_log(sub_section_title="General statistics")
    logging.info(descriptive_stats_table.to_latex(index=False))

    # -------- Descriptive Statistics for Lymph Nodes Involvement -------- #
    descriptive_table_lymph_nodes = descriptive_statistics.get_descriptive_stats_dataframe_from_specific_outcome(
        list_of_columns=list_of_columns,
        outcome=Outcomes.LYMPH_NODE.name
    )
    sub_section_title_log(sub_section_title="Descriptive Statistics for Lymph Nodes Involvement")
    logging.info(descriptive_table_lymph_nodes.to_latex(index=False))

    # -------- Descriptive Statistics for BCR Recurrence 5 years -------- #
    descriptive_table_bcr_5_years = descriptive_statistics.get_descriptive_stats_dataframe_from_specific_outcome(
        list_of_columns=list_of_columns,
        outcome=Outcomes.BCR_5YEARS.name
    )
    sub_section_title_log("Descriptive Statistics for BCR Recurrence 5 years")
    logging.info(descriptive_table_bcr_5_years.to_latex(index=False))

    # ----------------------------------------------------------------------------------------------------------- #
    #                                Frequency Tables and Test on Proportions                                     #
    # ----------------------------------------------------------------------------------------------------------- #
    section_title_log(section_title="Frequency Tables and Test on Proportions")

    # -------- General Frequency Table -------- #
    list_of_columns = [
        "Stade clinique",
        "Gleason global biopsie",
        "Gleason primaire biopsie",
        "Gleason secondaire biopsie",
        "pN",
        "Récurrence 5 ans (60 mois), oui = 1; non =0",
        "Récurrence 10 ans (120 mois), oui = 1; non =0",
    ]
    frequency_table = descriptive_statistics.get_frequency_table(list_of_columns=list_of_columns)

    sub_section_title_log(sub_section_title="General Frequency Table")
    logging.info(frequency_table.to_latex(index=False))

    # -------- Frequency Table for Lymph Nodes Involvement -------- #
    frequency_table_lymph_nodes = descriptive_statistics.get_frequency_table_and_test_on_proportions(
        list_of_columns=list_of_columns,
        outcome=Outcomes.BCR_5YEARS.name
    )
    sub_section_title_log(sub_section_title="Frequency Table for Lymph Nodes Involvement")
    logging.info(frequency_table_lymph_nodes.to_latex(index=False))

    # -------- Frequency Table for BCR Recurrence 5 years -------- #
    sub_section_title_log(sub_section_title="Frequency Table for BCR Recurrence 5 years")
    logging.info(frequency_table_lymph_nodes.to_latex(index=False))

