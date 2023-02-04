import json
import os
import time

from jss import JobShopSchedulingProblem, format_result
from sa import SA


class JssBenchmark:
    def __init__(self, folder_path, output_path):
        problems = []
        file_names = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

        for file_name in file_names:
            with open(os.path.join(folder_path, file_name)) as f:
                data = [x.strip().split(" ") for x in f.readlines()]
            jobs = [[(int(task[i]), int(task[i + 1])) for i in range(0, len(task), 2)] for task in data]
            problems.append([file_name, JobShopSchedulingProblem(jobs)])
        self.problems = problems
        self.output_path = output_path

    def run(self):
        results = []
        for problem in self.problems:
            file_name, jss_problem = problem
            with open(f'{self.output_path}/{file_name}', 'w') as f:
                print("Start Problem: ", file_name, file=f)
                st = time.time()
                best, S = SA(jss_problem, 1000., 0.000001)
                et = time.time()
                print("Best makespan: ", best, file=f)
                print("\nSolution (job_index, subtask_index, start, end):", file=f)
                print(format_result(S), file=f)
                elapsed_time = et - st
                print('Execution time:', elapsed_time, 'seconds', file=f)
                results.append({
                    "file": file_name,
                    "result": best,
                    "elapsed_seconds": elapsed_time
                })
        print(json.dumps(results, indent=4))
        print(f"Check '{self.output_path}' folder for more details regarding the results")
