import random
import numpy as np


# acceptance probability
def accept(current_cost, new_cost, T):
    if new_cost <= current_cost:
        return True
    if random.random() < np.exp(-(new_cost - current_cost) / T):
        return True
    else:
        return False


# cooling schedule
def updateTemperature(T, k):
    return T * 0.9995
    # return T/k


# Simulated Annealing algorithm
def SA(prob, T_Max, T_Min):
    S = prob.init_solution()
    S_cost = prob.eval(S)

    S_best = S
    S_best_cost = S_cost

    T = T_Max
    k = 0
    while T > T_Min:
        k = k + 1
        S_prim = prob.perturb_solution(S)
        S_prim_cost = prob.eval(S_prim)

        if accept(S_cost, S_prim_cost, T):
            S = S_prim.copy()
            S_cost = S_prim_cost
        if S_cost < S_best_cost:
            S_best = S.copy()
            S_best_cost = S_cost

        T = updateTemperature(T, k)

    return S_best_cost, S_best
