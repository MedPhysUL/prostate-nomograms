from prostate_cancer_nomograms.MSKCC.web_table_scraper import WebTableScraper
import pandas as pd


class BaseModel:

    def __init__(self, patients_dataframe: pd.DataFrame, model_name: str):
        super(BaseModel, self).__init__()
        self.patients_dataframe = patients_dataframe
        self.model_name = model_name

    @property
    def url(self):
        raise NotImplementedError()

    @property
    def json_folder_path(self):
        raise NotImplementedError()

    @property
    def variables_dataframe(self):
        variables_coefficients_table_scraper = WebTableScraper(
            url=self.url,
            json_folder_path=self.json_folder_path,
            variables_coefficients=True
        )
        variables_dataframe = variables_coefficients_table_scraper.dataframe
        variables_dataframe = variables_dataframe[variables_dataframe["Model"] == self.model_name]

        return variables_dataframe

    @property
    def spline_dataframe(self):
        spline_coefficients_table_scraper = WebTableScraper(
            url=self.url,
            json_folder_path=self.json_folder_path,
            spline_coefficients=True
        )
        spline_dataframe = spline_coefficients_table_scraper.dataframe

        return spline_dataframe
