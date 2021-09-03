import os
import logging

from prostate_cancer_nomograms.logging_tools import logs_file_setup, section_title_log, sub_section_title_log
from prostate_cancer_nomograms.statistical_analysis.outcomes import Outcomes
from prostate_cancer_nomograms.nomograms import Nomograms
from prostate_cancer_nomograms.root import PATH_TO_DATA_FOLDER
from prostate_cancer_nomograms.statistical_analysis.data_loaders.dataset_loader import DatasetLoader
from prostate_cancer_nomograms.statistical_analysis.descriptive_statistics.descriptive_statistics import \
    DescriptiveStatistics
from prostate_cancer_nomograms.statistical_analysis.nomograms_performance_evaluation.AUC import AUC
from prostate_cancer_nomograms.statistical_analysis.nomograms_performance_evaluation.calibration_curve import \
    CalibrationCurve
from prostate_cancer_nomograms.statistical_analysis.nomograms_performance_evaluation.DCA import DCA

# ----------------------------------------------------------------------------------------------------------- #
#                                              Logs Setup                                                     #
# ----------------------------------------------------------------------------------------------------------- #
logs_file_setup(__file__, logging.INFO)

# ----------------------------------------------------------------------------------------------------------- #
#                                             Data Loading                                                    #
# ----------------------------------------------------------------------------------------------------------- #
dataset_loader = DatasetLoader(
    path_to_dataset=os.path.join(PATH_TO_DATA_FOLDER, "CORES_DEPENDENT_results.csv")
)

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
    outcome=Outcomes.LYMPH_NODE_CORES.name
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

# ----------------------------------------------------------------------------------------------------------- #
#                                                AUC (MSKCC)                                                  #
# ----------------------------------------------------------------------------------------------------------- #
section_title_log(section_title="AUC (MSKCC)")
auc = AUC(dataframe=dataset, nomogram=Nomograms.MSKCC.name)

# -------- AUC for Lymph Nodes Involvement (MSKCC) -------- #
sub_section_title_log(sub_section_title="AUC for Lymph Nodes Involvement (MSKCC)")
auc_lymph_nodes_mskcc = auc.plot_auc(outcome=Outcomes.LYMPH_NODE_CORES.name)

# -------- AUC for BCR Recurrence 5 years -------- #
sub_section_title_log(sub_section_title="AUC for BCR Recurrence 5 years (MSKCC)")
auc_bcr_5years_mskcc = auc.plot_auc(outcome=Outcomes.BCR_5YEARS.name)

# ----------------------------------------------------------------------------------------------------------- #
#                                                AUC (CAPRA)                                                  #
# ----------------------------------------------------------------------------------------------------------- #
section_title_log(section_title="AUC (CAPRA)")

auc.nomogram = Nomograms.CAPRA.name

# -------- AUC for Lymph Nodes Involvement (CAPRA) -------- #
sub_section_title_log(sub_section_title="AUC for Lymph Nodes Involvement (CAPRA)")
auc_lymph_nodes_capra = auc.plot_auc(outcome=Outcomes.LYMPH_NODE_CORES.name)

# -------- AUC for BCR Recurrence 5 years (CAPRA) -------- #
sub_section_title_log(sub_section_title="AUC for BCR Recurrence 5 years (CAPRA)")
auc_bcr_5years_capra = auc.plot_auc(outcome=Outcomes.BCR_5YEARS.name)

# ----------------------------------------------------------------------------------------------------------- #
#                                          Calibration curve (MSKCC)                                          #
# ----------------------------------------------------------------------------------------------------------- #
section_title_log(section_title="Calibration curve (MSKCC)")
calibration_curve = CalibrationCurve(dataframe=dataset, nomogram=Nomograms.MSKCC.name)

# -------- Calibration curve for Lymph Nodes Involvement (MSKCC) -------- #
sub_section_title_log(sub_section_title="Calibration curve for Lymph Nodes Involvement (MSKCC)")
calibration_curve_lymph_nodes_mskcc = calibration_curve.plot_calibration_curve(outcome=Outcomes.LYMPH_NODE_CORES.name)

# -------- Calibration curve for BCR Recurrence 5 years -------- #
sub_section_title_log(sub_section_title="Calibration curve for BCR Recurrence 5 years (MSKCC)")
calibration_curve_bcr_5years_mskcc = calibration_curve.plot_calibration_curve(
    outcome=Outcomes.BCR_5YEARS.name,
    reverse_outcome=True
)

# ----------------------------------------------------------------------------------------------------------- #
#                                           Calibration curve (CAPRA)                                         #
# ----------------------------------------------------------------------------------------------------------- #
section_title_log(section_title="Calibration curve (CAPRA)")

calibration_curve.nomogram = Nomograms.CAPRA.name

# -------- Calibration curve for Lymph Nodes Involvement (CAPRA) -------- #
sub_section_title_log(sub_section_title="Calibration curve for Lymph Nodes Involvement (CAPRA)")
calibration_curve_lymph_nodes_capra = calibration_curve.plot_calibration_curve(outcome=Outcomes.LYMPH_NODE_CORES.name)

# -------- Calibration curve for BCR Recurrence 5 years (CAPRA) -------- #
sub_section_title_log(sub_section_title="Calibration curve for BCR Recurrence 5 years (CAPRA)")
calibration_curve_bcr_5years_capra = calibration_curve.plot_calibration_curve(
    outcome=Outcomes.BCR_5YEARS.name,
    reverse_outcome=True
)

# ----------------------------------------------------------------------------------------------------------- #
#                                     Decision curve analysis (MSKCC)                                         #
# ----------------------------------------------------------------------------------------------------------- #
section_title_log(section_title="Decision curve analysis (MSKCC)")
dca = DCA(dataframe=dataset, nomogram=Nomograms.MSKCC.name)

# -------- DCA for Lymph Nodes Involvement (MSKCC) -------- #
sub_section_title_log(sub_section_title="DCA for Lymph Nodes Involvement (MSKCC)")
dca_lymph_nodes_mskcc = dca.plot_dca(outcome=Outcomes.LYMPH_NODE_CORES.name)

# -------- DCA for BCR Recurrence 5 years (MSKCC) -------- #
sub_section_title_log(sub_section_title="DCA for BCR Recurrence 5 years (MSKCC)")
dca_bcr_5years_mskcc = dca.plot_dca(outcome=Outcomes.BCR_5YEARS.name)

# ----------------------------------------------------------------------------------------------------------- #
#                                     Decision curve analysis (CAPRA)                                         #
# ----------------------------------------------------------------------------------------------------------- #
section_title_log(section_title="Decision curve analysis (CAPRA)")
dca = DCA(dataframe=dataset, nomogram=Nomograms.CAPRA.name)

# -------- DCA for Lymph Nodes Involvement (CAPRA) -------- #
sub_section_title_log(sub_section_title="DCA for Lymph Nodes Involvement (CAPRA)")
dca_lymph_nodes_capra = dca.plot_dca(outcome=Outcomes.LYMPH_NODE_CORES.name)

# -------- DCA for BCR Recurrence 5 years (CAPRA) -------- #
sub_section_title_log(sub_section_title="DCA for BCR Recurrence 5 years (CAPRA)")
dca_bcr_5years_capra = dca.plot_dca(outcome=Outcomes.BCR_5YEARS.name)
