# Prostate Cancer Nomograms
A simple implementation of prostate cancer nomograms and some tools to perform statistical analysis on the predictions of these nomograms.

> Prostate cancer nomograms are prediction tools designed to help patients and their physicians understand the nature of their prostate cancer, assess risk based on specific characteristics of a patient and his disease, and predict the likely outcomes of treatment. <sup>[1][1]</sup>

## What is the purpose of this application?

Nomograms are typically implemented as web-based applications in which a physician must fill in certain boxes from a patient's medical information. Once all the boxes are filled in, the prediction tool can either calculate the probability of several clinical outcomes or calculate a risk score associated with the patient's health status, depending on the type of nomogram. The **purpose** of this application is to speed up the process for a very large number of patients. Indeed, the statistical models of the nomograms are reproduced in Python which allows to calculate in a few seconds the probabilities and the scores of thousands of patients. The coefficients of the models are read from the web sites, then used for the calculations. Statistical tools are also implemented to analyze the results directly with Python.

## What nomograms are currently implemented?

Currently, the nomograms of two major centers are implemented, namely :

1. Memorial Sloan Kettering Cancer Center (MSKCC)
   - [Pre-Radical Prostatectomy](https://www.mskcc.org/nomograms/prostate/pre_op)
   - [Post-Radical Prostatectomy](https://www.mskcc.org/nomograms/prostate/post_op)
2. UCSF - CAPRA
   - [CAPRA Score](https://urology.ucsf.edu/research/cancer/prostate-cancer-risk-assessment-and-the-ucsf-capra-score#.YS1Kqo5KiUk)

The two MSKCC nomograms directly give the probability and risk of different outcomes. The UCSF one gives a CAPRA score, which can be converted to probability using logistic regression on patient data.

## Disclaimer

This project was developed with the aim of being used for a very specific project requiring data analysis during my master's degree in physics at *Centre de recherche, CHU de Québec-Université Laval* and the generalization of the implementation was therefore not the (primary) objective. It is however a good starting point for anyone who wants to perform statistical analysis on nomograms developed as a web application.

## Getting started

#### Dataset structure

In the `data` folder, a `fake_dataset.xlsx` file allows the user to see how the dataset should be structured. Each information/column must be in your own dataset as the nomograms require this data.

#### Probabilities and score 

The script `__main__.py` is the main script to get a dataset with new columns containing the probabilities and score associated with each patient. Make sure to change the name of the file used to get the data. The default name is `fake_dataset.xlsx`. 

#### Statistical analysis

To perform a statistical analysis on a data set with previously determined probabilities and patient scores, go to the folder `prostate_cancer_nomograms\statistical_analysis` and run the `main_statistical_analysis.py` script. 

## References

[1]: <https://www.mskcc.org/nomograms/prostate> "MSKCC - Prostate Cancer Nomograms"
[2]: https://urology.ucsf.edu/research/cancer/prostate-cancer-risk-assessment-and-the-ucsf-capra-score "UCSF CAPRA - Prostate Cancer Nomograms"

## Contact

Maxence Larose, B. Ing., [maxence.larose.1@ulaval.ca](mailto:maxence.larose.1@ulaval.ca)

