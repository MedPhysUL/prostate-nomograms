import pandas as pd
import os
from sklearn.metrics import roc_curve, roc_auc_score, auc
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
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

clean_dataset = dataset[[
    "Âge au diagnostique",
    "PSA au diagnostique",
    "% cores POS",
    "% cores NEG",
    "PSA_valeur de récidive",
    "Durée de suivi (mois)",
    "Dernière PSA",
    "pN",
    "CAPRA Score",
    "Lymph Node Involvement (Cores)",

]]
clean_dataset = clean_dataset.replace("pN1", 1)
clean_dataset = clean_dataset.replace("pN0", 0)

clf = LogisticRegression().fit(
    X=np.array(clean_dataset["CAPRA Score"]).reshape(-1, 1),
    y=clean_dataset["pN"]
)

fpr, tpr, thresholds = roc_curve(
    y_true=clean_dataset["pN"],
    y_score=clf.predict_proba(X=np.array(clean_dataset["CAPRA Score"]).reshape(-1, 1))[:, 1],
    pos_label=1
)

auc_score = auc(
    x=fpr,
    y=tpr
)

plt.plot(fpr, tpr, color='darkorange', lw=2)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.show()

print(auc_score)

prob_true, prob_pred = calibration_curve(
    y_true=clean_dataset["pN"],
    y_prob=clf.predict_proba(X=np.array(clean_dataset["CAPRA Score"]).reshape(-1, 1))[:, 1],
    n_bins=5,
)

print(prob_pred)
print(prob_true)
plt.plot(prob_pred, prob_true, color="darkorange", lw=2)
plt.show()
