import pandas as pd
import numpy as np
from prostate_cancer_nomograms.MSKCC.base.base_logistic_regression_model import BaseLogisticRegressionModel


class LogisticRegressionModel(BaseLogisticRegressionModel):
    def __init__(
            self,
            patients_dataframe: pd.DataFrame,
            variables_dataframe: pd.DataFrame,
            spline_knots_dataframe: pd.DataFrame,
            model_name: str
    ):
        super(BaseLogisticRegressionModel, self).__init__(
            patients_dataframe=patients_dataframe,
            variables_dataframe=variables_dataframe,
            spline_knots_dataframe=spline_knots_dataframe
        )
        self.model_name = model_name

    @property
    def cores(self):
        if self.model_name.endswith("(Cores)"):
            return True
        else:
            return False

    @property
    def gleason_value(self) -> np.ndarray:
        primary_gleason = np.array(self.patients_information["Gleason primaire biopsie"])
        secondary_gleason = np.array(self.patients_information["Gleason secondaire biopsie"])
        total_gleason_score = primary_gleason + secondary_gleason

        gleason_value = np.zeros_like(total_gleason_score, dtype=float)
        mask_grade_2 = np.where(((primary_gleason == 3) & (secondary_gleason == 4)), True, False)
        mask_grade_3 = np.where(((primary_gleason == 4) & (secondary_gleason == 3)), True, False)

        gleason_value[mask_grade_2] = self.variables_values["Biopsy Gleason Grade Group 2"]
        gleason_value[mask_grade_3] = self.variables_values["Biopsy Gleason Grade Group 3"]
        gleason_value[total_gleason_score == 8] = self.variables_values["Biopsy Gleason Grade Group 4"]
        gleason_value[total_gleason_score == 9] = self.variables_values["Biopsy Gleason Grade Group 5"]
        gleason_value[total_gleason_score == 10] = self.variables_values["Biopsy Gleason Grade Group 5"]

        return gleason_value

    @property
    def clinical_stage_value(self):
        clinical_tumor_stage = self.patients_information["Stade clinique"]

        clinical_stage_value = np.zeros_like(clinical_tumor_stage, dtype=float)
        clinical_stage_value[list(map("T2a".__eq__, clinical_tumor_stage))] = self.variables_values["Clinical Stage 2A"]
        clinical_stage_value[list(map("T2b".__eq__, clinical_tumor_stage))] = self.variables_values["Clinical Stage 2B"]
        clinical_stage_value[list(map("T2c".__eq__, clinical_tumor_stage))] = self.variables_values["Clinical Stage 2C"]
        clinical_stage_value[list(map("T3a".__eq__, clinical_tumor_stage))] = self.variables_values["Clinical Stage 3+"]
        clinical_stage_value[list(map("T3b".__eq__, clinical_tumor_stage))] = self.variables_values["Clinical Stage 3+"]
        clinical_stage_value[list(map("T3c".__eq__, clinical_tumor_stage))] = self.variables_values["Clinical Stage 3+"]

        return clinical_stage_value

    @property
    def positive_cores_value(self):
        return np.array(self.patients_information["NbCtePositive"])*self.variables_values["No. of Positive Cores"]

    @property
    def negative_cores_value(self):
        return np.array(self.patients_information["NbCteNegative"])*self.variables_values["No. of Negative Cores"]

    @property
    def predicted_result(self):
        result = self.variables_values["Intercept"]
        result += np.array(self.patients_information["PSA au diagnostique"]) * self.variables_values["Preoperative PSA"]
        result += self.spline_term_1 * self.variables_values["Preoperative PSA Spline 1"]
        result += np.array(self.spline_term_2 * self.variables_values["Preoperative PSA Spline 2"], dtype=float)
        result += np.array(self.patients_information["Âge au diagnostique"]) * self.variables_values["Patient Age"]
        result += self.gleason_value
        result += self.clinical_stage_value

        if self.cores:
           result += self.positive_cores_value
           result += self.negative_cores_value

        return result
