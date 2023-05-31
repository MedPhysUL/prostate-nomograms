import numpy as np
from sklearn.linear_model import LogisticRegression as SklearnLogisticRegression


class LogisticRegression:

    def __init__(self, random_state: int = 0):
        """
        Logistic regression.

        Parameters
        ----------
        random_state : int
            The random state.
        """
        self.classifier = SklearnLogisticRegression(random_state=random_state)

    def fit(
            self,
            features: np.ndarray,
            target: np.ndarray
    ):
        """
        Fits the model.

        Parameters
        ----------
        features : numpy.ndarray
            The features.
        target : numpy.ndarray
            The outcome.
        """
        self.classifier.fit(X=features, y=target)

    def get_predicted_probability(
            self,
            features: np.ndarray,
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        features : numpy.ndarray
            The features.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        return self.classifier.predict_proba(X=features)[:, 1]
