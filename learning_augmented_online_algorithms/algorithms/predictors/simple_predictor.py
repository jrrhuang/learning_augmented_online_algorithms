from . import AbstractPredictor


class SimplePredictor(AbstractPredictor):
    """
    This predictor generates predictions by taking the largest exchange
    rate from the previous week.
    """
    def predict(self, data):
        """
        Given a time-series array of data, predicts the next value.

        Argument:
        data (list of list of floats) - time-series data to extrapolate from

        Returns:
        prediction (float) - estimation of next value in time-series
        """
        if len(data) > 0:
            return max(data[-1])
        return self.L
