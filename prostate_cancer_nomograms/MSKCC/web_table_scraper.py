import re
import json
import os
from typing import NamedTuple

import requests
import pandas as pd


class WebTableScraper:

    class Date(NamedTuple):
        day: str = None
        month: str = None
        year: str = None

    class DataframeKind(NamedTuple):
        table_index: int = None
        file_name: str = ""

    VariablesCoefficientsDataframeKind = DataframeKind(
        table_index=6,
        file_name="variables_coefficients"
    )

    SplineCoefficientsDataframeKind = DataframeKind(
        table_index=7,
        file_name="spline_coefficients"
    )

    def __init__(
            self,
            url,
            json_folder_path,
            variables_coefficients: bool = False,
            spline_coefficients: bool = False
    ):
        self.url = url
        self.json_folder_path = json_folder_path

        if not variables_coefficients and not spline_coefficients:
            raise ValueError("Either one of the parameters ['variables_coefficients', 'spline_coefficients'] must be "
                             "set to True.")

        self.variables_coefficients = variables_coefficients
        self.spline_coefficients = spline_coefficients

    @property
    def dataframe_kind(self):
        if self.variables_coefficients:
            return self.VariablesCoefficientsDataframeKind
        elif self.spline_coefficients:
            return self.SplineCoefficientsDataframeKind
        else:
            raise ValueError("Either one of the parameters ['variables_coefficients', 'spline_coefficients'] must be "
                             "set to True.")

    @property
    def url_content(self) -> str:
        url_content = requests.get(self.url).text

        return url_content

    @property
    def date(self) -> Date:
        last_update_match = re.search('Updated:(\s\w+\s\w+),(\s(\w+))', self.url_content)
        date_list = last_update_match.group(0).split()

        date = self.Date(day=date_list[2][:-1], month=date_list[1], year=date_list[3])

        return date

    @property
    def json_file_name(self):
        json_file_name = f"{self.json_folder_path}\\{self.dataframe_kind.file_name}_{self.date.day}_{self.date.month}" \
                         f"_{self.date.year}.json"

        return json_file_name

    @property
    def json_exists(self):
        if os.path.exists(self.json_file_name):
            return True
        else:
            return False

    def create_dataframe(self):
        tables = pd.read_html(self.url_content)
        dataframe = tables[self.dataframe_kind.table_index]

        dataframe.to_json(
            path_or_buf=self.json_file_name,
            orient="columns",
            indent=1
        )

    @property
    def dataframe(self):
        if self.json_exists:
            pass
        else:
            self.create_dataframe()

        with open(self.json_file_name) as file:
            models_coefficients = json.load(file)

        dataframe = pd.DataFrame.from_dict(models_coefficients, orient='columns')

        return dataframe


if __name__ == "__main__":
    url = "https://www.mskcc.org/nomograms/prostate/post_op/coefficients"
    web_scrapper = WebTableScraper(
        url,
        json_folder_path="post_radical_prostatectomy/models_coefficients",
        variables_coefficients=True
    )

    print(web_scrapper.dataframe)
