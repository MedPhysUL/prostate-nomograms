import pandas as pd
from MSKCC.post_radical_prostatectomy.post_radical_prostatectomy_model import PostRadicalProstatectomyModel

d = {'Age': [65, 80],
     'PSA': [40, 60],
     "Primary Gleason": [4, 3],
     "Secondary Gleason": [5, 5],
     "Surgical Margin Status": [True, False],
     "Extracapsular Extension": [False, True],
     "Seminal Vesicle Invasion": [True, False],
     "Lymph Node Involvement": [False, True],
     "Free Months": [24, 40]
     }

df = pd.DataFrame(data=d)

post_radical_prostatectomy_model = PostRadicalProstatectomyModel(
    patients_dataframe=df,
    model_name="Postoperative BCR"
)

print(post_radical_prostatectomy_model.get_predictions(number_of_years=5))
