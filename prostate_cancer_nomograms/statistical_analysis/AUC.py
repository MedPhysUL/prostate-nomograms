import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.metrics import roc_curve, roc_auc_score, auc
from sklearn.calibration import calibration_curve
from prostate_cancer_nomograms.root import PATH_TO_DATA_FOLDER

# Dataset preparation
dataset = pd.read_csv(
    filepath_or_buffer=os.path.join(PATH_TO_DATA_FOLDER, "PreOp_Cores_dependent_results.csv")
)

dataset.dropna(subset=["Gleason global biopsie"], inplace=True)
dataset = dataset[dataset["pN"] != "pNx"]
dataset = dataset[dataset["pN"] != "n/d"]
dataset["Récurrence 5 ans (60 mois), oui = 1; non =0"] = dataset["Récurrence 5 ans (60 mois), oui = 1; non =0"].fillna(0)
dataset["Récurrence 10 ans (120 mois), oui = 1; non =0"] = dataset["Récurrence 10 ans (120 mois), oui = 1; non =0"].fillna(0)
dataset["Récurrence 10 ans (120 mois), oui = 1; non =0"] = dataset["Récurrence 5 ans (60 mois), oui = 1; non =0"] + dataset["Récurrence 10 ans (120 mois), oui = 1; non =0"]

# Descriptive statistics
clean_dataset = dataset[[
    "Âge au diagnostique",
    "PSA au diagnostique",
    "% cores POS",
    "% cores NEG",
    "PSA_valeur de récidive",
    "Durée de suivi (mois)",
    "Dernière PSA",
    "pN",
    "Lymph Node Involvement (Cores)",

]]
clean_dataset = clean_dataset.replace("pN1", 1)
clean_dataset = clean_dataset.replace("pN0", 0)

print(np.array(clean_dataset["pN"]))
print(np.array(clean_dataset["Lymph Node Involvement (Cores)"]))

fpr, tpr, thresholds = roc_curve(
    y_true=np.array(clean_dataset["pN"]),
    y_score=np.array(clean_dataset["Lymph Node Involvement (Cores)"]),
    pos_label=1
)

auc_score = auc(
    x=fpr,
    y=tpr
)

print(auc_score)

plt.plot(fpr, tpr, color='darkorange', lw=2)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.show()

prob_true, prob_pred = calibration_curve(
    y_true=clean_dataset["pN"],
    y_prob=clean_dataset["Lymph Node Involvement (Cores)"],
    n_bins=10
)
print(prob_pred)
print(prob_true)
plt.plot(prob_pred, prob_true, color="darkorange", lw=2)
plt.show()
