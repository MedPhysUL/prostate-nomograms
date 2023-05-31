from enum import StrEnum


class Nomograms(StrEnum):
    MSKCC = "MSKCC"
    CAPRA = "CAPRA"


class ClassificationOutcome(StrEnum):
    EXTRACAPSULAR_EXTENSION = "Extracapsular Extension"
    EXTRACAPSULAR_EXTENSION_CORES = "Extracapsular Extension (Cores)"
    LYMPH_NODE_INVOLVEMENT = "Lymph Node Involvement"
    LYMPH_NODE_INVOLVEMENT_CORES = "Lymph Node Involvement (Cores)"
    ORGAN_CONFINED_DISEASE = "Organ Confined Disease"
    ORGAN_CONFINED_DISEASE_CORES = "Organ Confined Disease (Cores)"
    SEMINAL_VESICLE_INVASION = "Seminal Vesicle Invasion"
    SEMINAL_VESICLE_INVASION_CORES = "Seminal Vesicle Invasion (Cores)"


class SurvivalOutcome(StrEnum):
    CASTRATE_RESISTANT = "Castrate Resistant"
    CASTRATE_RESISTANT_CORES = "Castrate Resistant (Cores)"
    HORMONOTHERAPY = "Hormonotherapy"
    HORMONOTHERAPY_CORES = "Hormonotherapy (Cores)"
    METASTASIS = "Metastasis"
    METASTASIS_CORES = "Metastasis (Cores)"
    PREOPERATIVE_BCR = "Preoperative BCR"
    PREOPERATIVE_BCR_CORES = "Preoperative BCR (Cores)"
    PREOPERATIVE_PROSTATE_CANCER_DEATH = "Preoperative Prostate Cancer Death"
    PREOPERATIVE_PROSTATE_CANCER_DEATH_CORES = "Preoperative Prostate Cancer Death (Cores)"
