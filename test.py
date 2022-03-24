from learning_augmented_online_algorithms import OMSThresholdFunction
from learning_augmented_online_algorithms import BTCDataLoader

dl = BTCDataLoader()
for week_data in iter(dl):
    L, U = min(week_data), max(week_data)
    onemax_tf1 = OMSThresholdFunction(L, U, lmbda=0.0)
    onemax_tf2 = OMSThresholdFunction(L, U, lmbda=0.5)
    onemax_tf3 = OMSThresholdFunction(L, U, lmbda=1.0)
    w = 0
    for price in week_data:
        print("L, U", L, U)
        print("0.0 250: ", onemax_tf1(w, 250))
        print("0.0 275: ", onemax_tf1(w, 275))

        print("0.5 250: ", onemax_tf2(w, 250))
        print("0.5 275: ", onemax_tf2(w, 275))

        print("1.0 250: ", onemax_tf3(w, 250))
        print("1.0 275: ", onemax_tf3(w, 275))
        break
    break
