from enum import Enum
import json
import os
import re
from typing import NamedTuple, Union

import pandas as pd
import requests


class Date(NamedTuple):
    day: str = None
    month: str = None
    year: str = None


class DataframeCategory(NamedTuple):
    table_index: int = None
    file_name: str = ""


class CoefficientCategory(Enum):
    VARIABLES: str = "variables"
    SPLINE: str = "spline"


class WebTableScraper:
    """
    The web table scraper. It scrapes the web table and saves it as a json file.
    """

    VariablesCoefficientsDataframeCategory = DataframeCategory(
        table_index=6,
        file_name="variables_coefficients"
    )

    SplineCoefficientsDataframeCategory = DataframeCategory(
        table_index=7,
        file_name="spline_coefficients"
    )

    def __init__(
            self,
            url: str,
            json_folder_path: str
    ):
        """
        Initializes the WebTableScraper class.

        Parameters
        ----------
        url : str
            The url of the web table.
        json_folder_path : str
            The path of the folder where the json file will be saved.
        """
        self.url = url
        self.json_folder_path = json_folder_path

    @property
    def url_content(self) -> str:
        """
        The content of the url.

        Returns
        -------
        url_content : str
            The content of the url.
        """
        url_content = requests.get(self.url).text

        return url_content

    @property
    def date(self) -> Date:
        """
        The date of the last update.

        Returns
        -------
        date : Date
            The date of the last update.
        """
        last_update_match = re.search('Updated:(\s\w+\s\w+),(\s(\w+))', self.url_content)
        date_list = last_update_match.group(0).split()

        date = Date(day=date_list[2][:-1], month=date_list[1], year=date_list[3])

        return date

    def _get_dataframe_category(self, coefficient_category: CoefficientCategory) -> DataframeCategory:
        """
        The dataframe Category.

        Parameters
        ----------
        coefficient_category : CoefficientCategory
            The coefficient category.

        Returns
        -------
        dataframe_category : DataframeCategory
            The dataframe Category.
        """
        if coefficient_category == CoefficientCategory.VARIABLES:
            return self.VariablesCoefficientsDataframeCategory
        elif coefficient_category == CoefficientCategory.SPLINE:
            return self.SplineCoefficientsDataframeCategory
        else:
            raise ValueError(f"coefficient_category must be one of {CoefficientCategory}")

    def _get_json_file_path(self, dataframe_category: DataframeCategory) -> str:
        """
        The path of the json file.

        Parameters
        ----------
        dataframe_category : DataframeCategory
            The dataframe category.

        Returns
        -------
        json_file_path : str
            The path of the json file.
        """
        json_file_path = os.path.join(
            self.json_folder_path,
            f"{dataframe_category.file_name}_{self.date.day}_{self.date.month}_{self.date.year}.json"
        )

        return json_file_path

    def create_dataframe(self, dataframe_category: DataframeCategory, json_file_path: str) -> None:
        """
        Creates the dataframe and saves it as a json file.

        Parameters
        ----------
        dataframe_category : DataframeCategory
            The dataframe category.
        json_file_path : str
            The path of the json file.
        """
        if not os.path.exists(self.json_folder_path):
            os.makedirs(self.json_folder_path)

        tables = pd.read_html(self.url_content)
        dataframe = tables[dataframe_category.table_index]

        dataframe.to_json(
            path_or_buf=json_file_path,
            orient="columns",
            indent=1
        )

    def get_models_coefficients(self, coefficient_category: Union[str, CoefficientCategory]) -> pd.DataFrame:
        """
        Gets the models coefficients.

        Parameters
        ----------
        coefficient_category : Union[str, CoefficientCategory]
            The coefficient category.

        Returns
        -------
        dataframe : pd.DataFrame
            The models coefficients.
        """
        coefficient_category = CoefficientCategory(coefficient_category)
        dataframe_category = self._get_dataframe_category(coefficient_category)

        json_path = self._get_json_file_path(dataframe_category)
        if os.path.exists(json_path):
            pass
        else:
            self.create_dataframe(dataframe_category, json_path)

        with open(json_path) as file:
            models_coefficients = json.load(file)

        dataframe = pd.DataFrame.from_dict(models_coefficients, orient='columns')

        return dataframe


if __name__ == "__main__":
    url = "https://www.mskcc.org/nomograms/prostate/post_op/coefficients"
    web_scrapper = WebTableScraper(
        url,
        json_folder_path="post_radical_prostatectomy/models_coefficients",
    )

    print(web_scrapper.get_models_coefficients(coefficient_category="variables"))
