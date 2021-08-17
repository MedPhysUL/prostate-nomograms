from prostate_cancer_nomograms.utils import ExtendedEnum


class ModelName(ExtendedEnum):
    preoperative_BCR_cores = "Preoperative BCR (Cores)"
    preoperative_BCR = "Preoperative BCR"
    lymph_node_involvement_cores = "Lymph Node Involvement (Cores)"
    lymph_node_involvement = "Lymph Node Involvement"
    extracapsular_extension_cores = "Extracapsular Extension (Cores)"
    extracapsular_extension = "Extracapsular Extension"
    organ_confined_disease_cores = "Organ Confined Disease (Cores)"
    organ_confined_disease = "Organ Confined Disease"
    seminal_vesicle_invasion = "Seminal Vesicle Invasion"
    seminal_vesicle_invasion_cores = "Seminal Vesicle Invasion (Cores)"
