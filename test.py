# just tests that one-max-search and optimal-offline-algorithm work as expected

from learning_augmented_online_algorithms import BTCDataLoader
from learning_augmented_online_algorithms.algorithms import OneMaxSearchAlgorithm, OneWayTradingAlgorithm, OptimalOfflineAlgorithm
from learning_augmented_online_algorithms.algorithms.predictors import SimplePredictor

print("Loading BTC data...")
dl = BTCDataLoader()
print("Done loading data!")

ooa = OptimalOfflineAlgorithm()

cum_profit_ooa = []
cum_profit_oms = []
cum_profit_owt = []
thetas = []
prev_data = []
for week_data in iter(dl):

    if len(week_data) < 10: # some weeks don't have data, don't run it then
        continue
    L, U = min(week_data), max(week_data) # want to change eventually bc this is "data snooping"
    theta = U / L
    thetas.append(theta)
    oms3 = OneMaxSearchAlgorithm(L, U, lmbda=1.0, predictor=None)
    # owt = OneWayTradingAlgorithm(L, U, lmbda=1.0, predictor=SimplePredictor(L, U))

    res3 = oms3.allocate(week_data)
    # res4 = owt.allocate(week_data)
    res4 = {"profit": 0}
    res5 = ooa.allocate(week_data)

    # total allocation should be 1.0
    assert sum(res3['allocation']) == 1.0
    # assert sum(res4['allocation']) == 1.0
    assert sum(res5['allocation']) == 1.0
    # calculate profits
    print("profits -- oms: ", res3['profit'], ", owt: ", res4['profit'], ", ooa: ", res5['profit'])

    # cumulative profits
    cum_profit_oms.append(res3['profit'])
    cum_profit_ooa.append(res5['profit'])

    prev_data.append(week_data)
print(" --- done ---")
print("profit ratio of oms: ", sum(cum_profit_oms) / sum(cum_profit_ooa))
print("average theta: ", sum(thetas) / len(thetas))
