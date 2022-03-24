from abc import abstractmethod


class AbstractPredictor:
    """
    Predictor that can be used in conjunction with the augmented online
    algorithms. Generates predictions from data, which may be used in
    full or in part in the augmented online algorithms.
    """
    @abstractmethod
    def __init__(self):
        """
        Initialization steps of predictor.
        """
        pass
    
    @abstractmethod
    def predict(self, arr):
        """
        Given a time-series array of data, predicts the next value.

        Argument:
        arr (list of floats) - time-series data to extrapolate from

        Returns:
        prediction (float) - estimation of next value in time-series
        """
        pass
