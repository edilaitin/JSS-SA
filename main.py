from jss import JobShopSchedulingProblem, print_result
from sa import SA

jobs_data = [  # task = (machine_id, processing_time).
    [(0, 3), (1, 2), (2, 2)],  # Job0
    [(0, 2), (2, 1), (1, 4)],  # Job1
    [(1, 4), (2, 3)]  # Job2
]
prob = JobShopSchedulingProblem(jobs_data)

best, S = SA(prob, 1000., 0.000001)
print("Best makespan: ", best)
print("\nSolution (job_index, subtask_index, start, end):")
print_result(S)
