# Prostate Nomograms

A simple implementation of prostate cancer nomograms.

> Prostate cancer nomograms are prediction tools designed to help patients and their physicians understand the nature of their prostate cancer, assess risk based on specific characteristics of a patient and his disease, and predict the likely outcomes of treatment. <sup>[1][1]</sup>

## Installation

### Latest stable version :

```
pip install prostate-nomograms
```

### Latest (possibly unstable) version :

```
pip install git+https://github.com/MaxenceLarose/prostate-cancer-nomograms
```

## What is the purpose of this application?

Nomograms are typically implemented as web-based applications in which a physician must fill in certain boxes using a patient's medical information. Once all the boxes are filled in, the prediction tool can either calculate the probability of several clinical outcomes or calculate a risk score associated with the patient's health status, depending on the type of nomogram. The **purpose** of this application is to speed up the process for a very large number of patients. Indeed, the statistical models of the nomograms are reproduced in Python which allows to calculate in a few seconds the probabilities and the scores of thousands of patients. The coefficients of the models are read from the web sites, then used for the calculations.

## Which nomograms are currently implemented?

Currently, the nomograms of two major centers are implemented, namely :

1. Memorial Sloan Kettering Cancer Center (MSKCC)
   - [Pre-Radical Prostatectomy](https://www.mskcc.org/nomograms/prostate/pre_op)
2. UCSF - CAPRA
   - [CAPRA Score](https://urology.ucsf.edu/research/cancer/prostate-cancer-risk-assessment-and-the-ucsf-capra-score#.YS1Kqo5KiUk)

The MSKCC nomogram directly gives the probability and risk of different outcomes. The UCSF one gives a CAPRA score, which is then converted to probability using logistic regression or cox regression on patient data.

Note that a custom nomogram is also implemented, i.e. a simple logistic regression or cox regression using arbitrary variables. 

## Getting started

You can find examples [here](https://github.com/MaxenceLarose/ProstateCancerNomograms/tree/main/examples).

## License

This code is provided under the [Apache License 2.0](https://github.com/MaxenceLarose/delia/blob/main/LICENSE).

## Citation

```
@misc{prostate-nomograms,
  title={prostate-nomograms: Prediction tools based on existing prostate cancer nomograms},
  author={Maxence Larose},
  year={2022},
  publisher={Université Laval},
  url={https://github.com/MaxenceLarose/prostate-nomograms},
}
```

## Contact

Maxence Larose, B. Ing., [maxence.larose.1@ulaval.ca](mailto:maxence.larose.1@ulaval.ca)

[comment]: REFERENCES>
[1]: <https://www.mskcc.org/nomograms/prostate> "MSKCC - Prostate Cancer Nomograms"
