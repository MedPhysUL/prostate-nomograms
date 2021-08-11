from prostate_cancer_nomograms.utils import ExtendedEnum


class ModelName(ExtendedEnum):
    preoperative_BCR_cores = "Preoperative BCR (Cores)"
    preoperative_BCR = "Preoperative BCR"
    lymph_node_involvement_cores = "Lymph Node Involvement (Cores)"
    lymph_node_involvement = "Lymph Node Involvement"
