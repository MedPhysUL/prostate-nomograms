import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class CAPRA:

    def __init__(self, patients_dataframe: pd.DataFrame):
        self.patients_dataframe = patients_dataframe

    @property
    def patients_information(self):
        return self.patients_dataframe.to_dict(orient="list")

    @property
    def age_score(self) -> np.ndarray:
        age = np.array(self.patients_information["âge au dx"])
        age_score = np.zeros_like(age, dtype=float)

        age_score[age < 50] = 0
        age_score[age >= 50] = 1

        return age_score

    @property
    def psa_score(self) -> np.ndarray:
        psa = np.array(self.patients_information["Diag_PSA"])
        psa_score = np.zeros_like(psa, dtype=float)

        psa_score[psa < 6] = 0
        psa_score[(6 <= psa) & (psa < 10)] = 1
        psa_score[(10 <= psa) & (psa < 20)] = 2
        psa_score[(20 <= psa) & (psa < 30)] = 3
        psa_score[psa >= 30] = 4

        return psa_score

    @property
    def gleason_score(self) -> np.ndarray:
        primary_gleason = np.array(self.patients_information["Gleason primaire Bx"])
        secondary_gleason = np.array(self.patients_information["Gleason secondaire Bx"])
        total_gleason_score = primary_gleason + secondary_gleason

        gleason_score = np.zeros_like(total_gleason_score, dtype=float)

        gleason_score[(secondary_gleason == 4) | (secondary_gleason == 5)] = 1
        gleason_score[(primary_gleason == 4) | (primary_gleason == 5)] = 3

        return gleason_score

    @property
    def clinical_stage_score(self) -> np.ndarray:
        clinical_tumor_stage = self.patients_information["Stade clinique"]

        clinical_stage_score = np.zeros_like(clinical_tumor_stage, dtype=float)
        clinical_stage_score[list(map("cT3a".__eq__, clinical_tumor_stage))] = 1
        clinical_stage_score[list(map("cT3b".__eq__, clinical_tumor_stage))] = 1
        clinical_stage_score[list(map("cT3c".__eq__, clinical_tumor_stage))] = 1

        return clinical_stage_score

    @property
    def positive_cores_score(self) -> np.ndarray:
        positive_cores_percentage = np.array(self.patients_information["% cores POS"])

        positive_cores_score = np.zeros_like(positive_cores_percentage, dtype=float)
        positive_cores_score[positive_cores_percentage >= 34] = 1

        return positive_cores_score

    def get_capra_score(self) -> np.ndarray:
        capra_score = self.age_score
        capra_score += self.psa_score
        capra_score += self.gleason_score
        capra_score += self.clinical_stage_score
        capra_score += self.positive_cores_score

        return capra_score

    def show_histogram(self) -> None:
        plt.hist(self.get_capra_score(), bins=20)
        plt.show()
