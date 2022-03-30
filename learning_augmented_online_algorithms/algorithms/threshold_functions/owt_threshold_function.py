from ctypes import ArgumentError
from .abstract_threshold_function import AbstractThresholdFunction
import numpy as np
import scipy.integrate as integrate
from scipy.special import lambertw
from scipy.optimize import fsolve

class OWTThresholdFunction(AbstractThresholdFunction):
    """
    Threshold function for one-way-trading, in which the algorithm
    is able to exchange any fraction of its resources and uses the
    threshold to optimally decide this amount.
    """
    def __init__(self, L, U, lmbda=1.0):
        super().__init__(L, U, lmbda)

        # alpha is the optimal competitive ratio
        self.alpha = np.real(1 + lambertw((self.theta - 1) / np.exp(1)))

        # Compute gamma and eta
        self.gamma = self.alpha + (1 - lmbda) * (self.theta - self.alpha)
        self.eta = self.theta / (self.theta / self.gamma + (self.theta - 1)
                                 * (1 - 1 / self.gamma * np.log((self.theta - 1) / (self.gamma - 1))))


    def __call__(self, w, pred):
        """
        Use calculated gamma and eta to determine threshold functions based on
        prediction of next price. Note that the resource allocation is being used,
        as one-way-trading allows for trading any fraction of the remaining resources
        (in [0, 1-w]).
        Arguments:
        w (float) - number between 0.0 to 1.0 denoting the fraction of resources
            already used.
        pred (float) - prediction of the price of the next time step, which may
            come from an ML model.
        Returns:
        reservation price (float): when price exceeds reservation price in
            one-max-search, a trade is executed.
        """
        if pred is None and self.lmbda < 1.0:
            raise TypeError("cannot use threshold function with "
                            "lmbda < 1.0 when there is no prediction")
        elif pred is None:
            # Default to pure online algorithm
            return self.L + (self.alpha * self.L - self.L) * np.exp(self.alpha * w)
        # clip if prediction is out of bounds
        pred = np.clip(pred, self.L, self.U)

        # pred now bounded between L and U
        # we now solve for the bounds used in the piecewise function for computing the threshold
        # solve for M and B
        def eq1(x):
            return [x[0] - self.L - (self.eta * self.L - self.L) * np.exp(self.eta * x[1]),
                    x[0] * self.gamma / self.eta - self.L - (self.U - self.L) * np.exp(self.gamma * (x[1] - 1))]
        M, B = fsolve(eq1, [20000,0.5])

        # solve for M1, B1, B1_, and B2
        def eq2(x):
            return [np.real(x[1] - 1 / self.gamma * np.log((max(x[0] / self.L, self.gamma) - 1) / (self.gamma - 1))),
                    np.real(x[0] / self.eta - integrate.quad(lambda u: self.L + (self.alpha * self.L - self.L) * np.exp(self.alpha * u), 0, x[1])[0] - (x[2] - x[1]) * x[0] - (1 - x[2]) * self.L),
                    np.real(pred - self.L - (x[0] - self.L) * np.exp(self.eta * (x[3] - x[2]))),
                    np.real(x[3] - 1 - 1 / self.gamma * np.log((min(pred * self.gamma / self.eta, self.U) - self.L) / (self.U - self.L)))]
        M1, B1, B1_, B2 = fsolve(eq2, [20000,0.5,0.5,0.5])

        # compute threshold using M, B, M1, B1, B1_, and B2
        if pred >= self.L and pred < M:
            if w >= 0 and w < B:
                return self.L + (self.eta * self.L - self.L) * np.exp(self.eta * w)
            else:
                return self.L + (self.U - self.L) * np.exp(self.gamma * (w - 1))
        else:
            if w >= 0 and w < B1:
                return self.L + (self.gamma * self.L - self.L) * np.exp(self.gamma * w)
            elif w >= B1 and w < B1_:
                return M1
            elif w >= B1_ and w <= B2:
                return self.L + (M1 - self.L) * np.exp(self.eta * (w - B1_))
            else:
                return self.L + (self.U - self.L) * np.exp(self.gamma * (w - 1))