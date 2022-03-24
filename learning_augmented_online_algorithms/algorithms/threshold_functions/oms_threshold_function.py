from learning_augmented_online_algorithms.algorithms.threshold_functions.abstract_threshold_function import AbstractThresholdFunction


class OMSThresholdFunction(AbstractThresholdFunction):
    """
    Threshold function for one-max-search, in which the algorithm
    simply uses all resources the first time when the price exceeds
    the reservation price.
    """
    def __init__(self, L, U, lmbda=1.0):
        super().__init__(L, U, lmbda)

        # parameter used to handle edge cases near 0 and 1
        self.eps = 1e-3

        # majority case use formula provided
        if lmbda > self.eps:
            self.gamma = (((1 - lmbda) ** 2 + 4 * lmbda * self.theta) ** .5 - (1 - lmbda)) / (2 * lmbda)
        # handle case where lmbda is near 0
        else:
            # in the limit to zero, gamma is equal to theta
            self.gamma = self.theta

        self.eta = self.theta / self.gamma
    
    
    def __call__(self, w, pred):
        """
        Use calculated gamma and eta to determine threshold functions based on
        prediction of next price. Notice that the resource allocation is not used,
        as one-max-search assumes either no trade has been made (w = 0) or a trade
        has been made (w = 1) without any in-between.

        Arguments:
        w (float) - number between 0.0 to 1.0 denoting the fraction of resources
            already used.
        pred (float) - prediction of the price of the next time step, which may
            come from an ML model.

        Returns:
        reservation price (float): when price exceeds reservation price in
            one-max-search, a trade is executed.
        """
        if pred >= self.L and pred < self.L * self.eta:
            return self.L * self.eta
        if pred >= self.L * self.eta and pred < self.L * self.gamma:
            return self.lmbda * self.L * self.gamma + (1 - self.lmbda) * pred / self.eta
        if pred >= self.L * self.gamma and pred <= self.U:
            return self.L * self.gamma
