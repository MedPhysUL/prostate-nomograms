import pandas as pd
from root import *

dataset = pd.read_csv(
    filepath_or_buffer=os.path.join(PATH_TO_DATA_FOLDER, "PreOp_Cores_dependent_results.csv")
)

clean_dataset = dataset[[
    "Âge au diagnostique",
    "PSA au diagnostique",
    "% cores POS",
    "% cores NEG",
    "PSA_valeur de récidive",
    "Durée de suivi (mois)",
    "Dernière PSA",
    "pN"
]]

print(clean_dataset)
print(clean_dataset.describe())
