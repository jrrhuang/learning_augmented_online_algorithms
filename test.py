# just tests that one-max-search and optimal-offline-algorithm work as expected

from learning_augmented_online_algorithms import BTCDataLoader
from learning_augmented_online_algorithms.algorithms import OneMaxSearchAlgorithm, OptimalOfflineAlgorithm

dl = BTCDataLoader()

ooa = OptimalOfflineAlgorithm()

actual_competitive_ratios = []
thetas = []
for week_data in iter(dl):

    if len(week_data) < 10: # some weeks don't have data, don't run it then
        continue
    L, U = min(week_data), max(week_data) # want to change eventually bc this is "data snooping"
    theta = U / L
    thetas.append(theta)
    oms3 = OneMaxSearchAlgorithm(L, U, lmbda=1.0, predictor=None)

    res3 = oms3.allocate(week_data)
    res4 = ooa.allocate(week_data)

    # total allocation should be 1.0
    assert sum(res3['allocation']) == 1.0
    assert sum(res4['allocation']) == 1.0
    # calculate profits
    print("profits: ", res3['profit'], res4['profit'])

    ratio = res4['profit'] / res3['profit']
    # practical competitive ratio calculation
    actual_competitive_ratios.append(ratio)
print(" --- done ---")
print("average competitive ratio: ", sum(actual_competitive_ratios) / len(actual_competitive_ratios))
print("average theta: ", sum(thetas) / len(thetas))
