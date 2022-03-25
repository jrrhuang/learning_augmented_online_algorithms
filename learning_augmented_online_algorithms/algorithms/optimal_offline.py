from .abstract_algorithm import AbstractAlgorithm

import numpy as np


class OptimalOfflineAlgorithm(AbstractAlgorithm):
    """
    The baseline offline algorithm which can see all the timesteps at the same
    time and allocate at the maximum price. This is the ideal case, and the ratio
    of its profit with another algorithm's profit is deemed the competitive ratio.
    The lower the competitive ratio and the closer it is to 1.0, the better.
    """
    def allocate(self, instance):
        """
        Runs algorithm on an instance of data, allocating resources to maximize
        profit.

        Arguments:
        instance : pd.Series
            - array of time-series prices, for example, one week of BTC prices

        Returns: result (dictionary)
        - result['allocation'] : list showing allocation at each time step, should
            sum up to 1.0, the total amount allowed to be allocated
        - result['profit'] : profit generated by the algorithm
        """
        result = {}

        allocation = np.zeros(shape=(len(instance),), dtype=np.float32)
        # allocate when the price is maximum
        argmax = instance.argmax()
        allocation[argmax] = 1.0
        result['allocation'] = allocation

        # profit is the highest price
        result['profit'] = instance[argmax]

        return result
