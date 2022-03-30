from abc import abstractmethod


class AbstractPredictor:
    """
    Predictor that can be used in conjunction with the augmented online
    algorithms. Generates predictions from data, which may be used in
    full or in part in the augmented online algorithms.
    """
    @abstractmethod
    def __init__(self, L, U):
        """
        Initialization steps of predictor.
        """
        self.L = L
        self.U = U
    
    @abstractmethod
    def predict(self, data):
        """
        Given a time-series array of data, predicts the next value.

        Argument:
        data (list of list of floats) - time-series data to extrapolate from

        Returns:
        prediction (float) - estimation of next value in time-series
        """
        pass
