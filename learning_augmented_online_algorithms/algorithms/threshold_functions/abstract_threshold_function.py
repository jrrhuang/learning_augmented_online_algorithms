from abc import abstractmethod


class AbstractThresholdFunction:
    """
    Online threshold-based algorithms (OTA) are a class of reserve-and-greedy
    algorithms, which use a threshold function to determine the amount of
    resources that need to be reserved, while the rest can be greedily
    allocated. This abstract class provides the skeleton for one-max-search
    and one-way-trading threshold functions. Assumes that prices can
    arbitrarily bounded.
    """
    def __init__(self, L, U, lmbda):
        """
        Initialize threshold function using lambda, a robustness parameter
        between 0.0 and 1.0. When lambda is close to 0.0, the threshold
        function relies more on a prediction, which may come from an ML model.
        When lambda is close to 1.0, the threshold function distrusts the
        prediction and utilizes the optimal result derived from purely
        algorithmic means.

        Arguments:
        U (float) - highest price bound
        L (float) - lowest price bound
        lmbda (float) - distrust parameter between 0.0 and 1.0
        """
        assert L > 0 and U > L
        assert 0.0 <= lmbda and lmbda <= 1.0

        self.L = L
        self.U = U
        self.theta = U / L
        self.lmbda = lmbda

    @abstractmethod
    def __call__(self, w, pred):
        """
        Takes as input the resource utilization w and outputs the reservation
        price when the resource utilization is w. The reservation price is
        defined as the price needed to be exceed to execute a trade.

        Arguments:
        w (float) - number between 0.0 to 1.0 denoting the fraction of resources
            already used
        pred (float) - prediction of the price of the next time step, which may
            come from an ML model
        """
        pass
