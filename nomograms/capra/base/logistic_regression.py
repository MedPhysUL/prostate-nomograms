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
            capra_score: np.ndarray,
            target: np.ndarray
    ):
        """
        Fits the model.

        Parameters
        ----------
        capra_score : numpy.ndarray
            The CAPRA score.
        target : numpy.ndarray
            The outcome.
        """
        self.classifier.fit(X=capra_score.reshape(-1, 1), y=target)

    def get_predicted_probability(
            self,
            capra_score: np.ndarray,
    ) -> np.array:
        """
        Gets the predicted result.

        Parameters
        ----------
        capra_score : numpy.ndarray
            The CAPRA score.

        Returns
        -------
        predicted_probability : numpy.ndarray
            The predicted probability.
        """
        return self.classifier.predict_proba(X=capra_score.reshape(-1, 1))[:, 1]
