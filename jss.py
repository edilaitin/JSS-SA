from operator import itemgetter
import copy
import random
import itertools


class JobShopSchedulingProblem:
    def __init__(self, jobs):
        jobs_flatten = []
        for x in range(len(jobs)):
            for y in range(len(jobs[x])):
                jobs_flatten.append([x, y, jobs[x][y][0], jobs[x][y][1]])
        self.jobs = jobs_flatten
        machines_count = max(self.jobs, key=itemgetter(2))[2] + 1  # find how many machines are there
        self.machines_count = machines_count

    def init_solution(self):
        return [self.jobs, self.schedule(self.jobs, self.machines_count)]

    def perturb_solution(self, solution):
        jobs, schedule = solution
        machines_count = max(jobs, key=itemgetter(2))[2] + 1  # find how many machines are there
        while True:
            first_job, second_job = random.choice(jobs), random.choice(jobs)
            # check if job_number is different
            if first_job[0] != second_job[0]:
                # indexes of two elements
                a, b = jobs.index(first_job), jobs.index(second_job)
                # indexes of previous jobs
                a_prev, b_prev = self.find_prev_index(jobs, first_job), self.find_prev_index(jobs, second_job)
                # check if the order of jobs are still valid
                if (a_prev is None or a_prev <= b) and (b_prev is None or b_prev <= a):
                    jobs_copy = copy.deepcopy(jobs)
                    jobs_copy[b], jobs_copy[a] = jobs_copy[a], jobs_copy[b]  # swap jobs
                    schedule_jobs = self.schedule(jobs_copy, machines_count)
                    if self.check_valid_schedule(schedule_jobs):
                        return [jobs_copy, schedule_jobs]

    def eval(self, solution):
        jobs, schedule = solution
        makespan = 0
        for machine_schedule in schedule:
            end_job = max(machine_schedule, key=itemgetter(2))[2]
            if makespan < end_job:
                makespan = end_job
        return makespan

    # creates schedule out of a ordered job list
    def schedule(self, jobs, machine_count):
        # first parameter is machine number
        results = [[] for x in range(machine_count)]
        time = [0] * (len(jobs) + 1)  # time of end of job
        time_m = [0] * machine_count  # time end of machine last job
        for job in jobs:
            job_n = job[0]  # job number
            machine_n = job[2]  # machine number
            duration = job[3]  # duration length
            # starting time is max(end of prev task in job, end of prev task on machine)
            start = max(time_m[machine_n], time[job_n])
            results[machine_n].append((job, start, start + duration))  # insert to the end
            # update the last time of job and machine
            time[job_n] = start + duration  # set new time of end of job
            time_m[machine_n] = start + duration  # set new end of last job of machine
        return results

    def find_prev_index(self, jobs, job):
        job_n = job[0]
        job_seq = job[1] - 1
        if job_seq < 0:
            return None
        for i in range(0, len(jobs)):
            if jobs[i][0] == job_n and jobs[i][1] == job_seq:
                return i

    def check_valid_schedule(self, schedule):
        flatten = list(itertools.chain(*schedule))
        sorted_jobs = sorted(flatten, key=lambda x: (x[0][0], x[0][1]))
        for i in range(len(sorted_jobs)):
            if i > 0 and sorted_jobs[i - 1][0][0] == sorted_jobs[i][0][0]:
                if sorted_jobs[i - 1][2] > sorted_jobs[i][1]:
                    return False
        return True


# function that returns schedule as readable output
def format_result(solution):
    jobs, schedule = solution
    i = 0
    result = ''
    for machine in schedule:
        string = "machine " + str(i) + " : "
        for job in machine:
            string = string + "(" + str(job[0][0]) + ", " + str(job[0][1]) + ", " + str(job[1]) + ", " + str(
                job[2]) + ") "
        result = result + string + '\n'
        i += 1
    return result
