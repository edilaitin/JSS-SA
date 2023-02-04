# JSS-SA
Job Shop Scheduling Implementation using Simulated Annealing

Run main.py to obtain the results for each problem instance. To add a new instance create a new file in the 'data' folder

# Problem definition example

TXT files of form 
```txt
0 3 1 2 2 2
0 2 2 1 1 4
1 4 2 3
```

Which maps (internally) to
```txt
jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 4)],  # Job1
    [(1, 4), (2, 3)]  # Job2
]
```

# Result example
```txt
Start Problem:  3x3.txt
Best makespan:  11

Solution (job_index, subtask_index, start, end):
machine 0 : (0, 0, 0, 3) (1, 0, 3, 5) 
machine 1 : (2, 0, 0, 4) (0, 1, 4, 6) (1, 2, 6, 10) 
machine 2 : (1, 1, 5, 6) (2, 1, 6, 9) (0, 2, 9, 11) 

Execution time: 2.328125476837158 seconds
```

# Simulated Annealing implementation
```python
import random
import numpy as np

def accept(current_cost, new_cost, T):
    if new_cost <= current_cost:
        return True
    if random.random() < np.exp(-(new_cost - current_cost) / T):
        return True
    else:
        return False

def updateTemperature(T, k):
    return T * 0.9995

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
```