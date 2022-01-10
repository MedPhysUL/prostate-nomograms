import pandas as pd


class DatasetLoader:

    def __init__(self, path_to_dataset: str):
        self.path_to_dataset = path_to_dataset

    @property
    def dataset(self):
        if self.path_to_dataset.endswith(".csv"):
            dataset = pd.read_csv(filepath_or_buffer=self.path_to_dataset)
        else:
            dataset = pd.read_excel(self.path_to_dataset)

        dataset = self.get_clean_dataset(dataset=dataset)

        return dataset

    @staticmethod
    def get_clean_dataset(dataset: pd.DataFrame):
        dataset.dropna(subset=["Gleason global biopsie"], inplace=True)

        dataset = dataset[dataset["pN"] != "pNx"]
        dataset = dataset[dataset["pN"] != "n/d"]

        dataset["Récurrence 5 ans (60 mois) oui = 1 non =0"].fillna(0, inplace=True)
        dataset["Récurrence 10 ans (120 mois) oui = 1; non =0"].fillna(0, inplace=True)
        mask_5years_reccurence = dataset["Récurrence 5 ans (60 mois) oui = 1 non =0"]
        mask_10years_reccurence = dataset["Récurrence 10 ans (120 mois) oui = 1; non =0"]
        dataset["Récurrence 10 ans (120 mois) oui = 1; non =0"] = mask_5years_reccurence + mask_10years_reccurence

        return dataset
