import os
from prostate_cancer_nomograms.root import PATH_TO_DATA_FOLDER
from prostate_cancer_nomograms.statistical_analysis.dataset_loader import DatasetLoader
from prostate_cancer_nomograms.statistical_analysis.descriptive_statistics import DescriptiveStatistics


dataset_loader = DatasetLoader(path_to_dataset=os.path.join(PATH_TO_DATA_FOLDER, "PreOp_Cores_dependent_results.csv"))
dataset = dataset_loader.dataset


descriptive_statistics = DescriptiveStatistics(dataset=dataset)
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
print(descriptive_stats_table.to_latex(index=True))

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
print(frequency_table.to_latex(index=False))

proportions_freq = descriptive_statistics.get_frequency_table_and_test_on_proportions(list_of_columns=list_of_columns)
print(proportions_freq.to_latex(index=False))

descriptive_statistics.print_pN0_frequency_table(list_of_columns=list_of_columns)
descriptive_statistics.print_pN1_frequency_table(list_of_columns=list_of_columns)
descriptive_statistics.pN_frequency_table(column_name="Gleason global biopsie")
descriptive_statistics.chi2_test_on_frequency_table(column_name="Gleason global biopsie")
descriptive_statistics.mannwhitneyu_test(column_name="Âge au diagnostique")
