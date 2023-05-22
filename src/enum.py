from enum import StrEnum


class Nomograms(StrEnum):
    MSKCC = "MSKCC"
    CAPRA = "CAPRA"


class Outcome(StrEnum):
    EXTRACAPSULAR_EXTENSION = "Extracapsular Extension"
    EXTRACAPSULAR_EXTENSION_CORES = "Extracapsular Extension (Cores)"
    LYMPH_NODE_INVOLVEMENT = "Lymph Node Involvement"
    LYMPH_NODE_INVOLVEMENT_CORES = "Lymph Node Involvement (Cores)"
    ORGAN_CONFINED_DISEASE = "Organ Confined Disease"
    ORGAN_CONFINED_DISEASE_CORES = "Organ Confined Disease (Cores)"
    PREOPERATIVE_BCR = "Preoperative BCR"
    PREOPERATIVE_BCR_CORES = "Preoperative BCR (Cores)"
    PREOPERATIVE_PROSTATE_CANCER_DEATH = "Preoperative Prostate Cancer Death"
    PREOPERATIVE_PROSTATE_CANCER_DEATH_CORES = "Preoperative Prostate Cancer Death (Cores)"
    SEMINAL_VESICLE_INVASION = "Seminal Vesicle Invasion"
    SEMINAL_VESICLE_INVASION_CORES = "Seminal Vesicle Invasion (Cores)"


class SurvivalOutcome(StrEnum):
    PREOPERATIVE_BCR = "Preoperative BCR"
    PREOPERATIVE_BCR_CORES = "Preoperative BCR (Cores)"
    PREOPERATIVE_PROSTATE_CANCER_DEATH = "Preoperative Prostate Cancer Death"
    PREOPERATIVE_PROSTATE_CANCER_DEATH_CORES = "Preoperative Prostate Cancer Death (Cores)"
