from Machine import Process, process_generator
import time


class FCFS:
    tmp_queue = []
    current_time = 0

    ready_queue = []
    gantt = []
    turnaround_time = []
    pid_turn_time = []
    response_time = []
    waiting_time = []
    pid_response_time = []

    def __init__(self, lst):
        self.process_list = lst
        self.waiting_time = [0 for i in range(len(self.process_list))]

    def search(self, pid):
        for p in self.process_list:
            if p.p_id == pid:
                return p

    def run(self):
        for i in range(len(self.process_list)):
            p = self.process_list[i]
            if p.io_time == 0:
                self.tmp_queue.append((p.arrival_time, p.p_id, p.cpu_burst2 + p.cpu_burst1, "cpu_2"))
            else:
                self.tmp_queue.append(
                    (p.arrival_time, p.p_id, p.cpu_burst1, "cpu_1"))  # ( arrival_time, p_id, cpu_burst1)

        while len(self.tmp_queue) != 0:
            # sort based on arrival_time if equal --> sort based on p_id
            self.tmp_queue = sorted(self.tmp_queue)
            value = self.tmp_queue.pop(0)

            if self.current_time < value[0]:  # add idle time waiting for next process to come
                idle_time = value[0] - self.current_time
                self.current_time += idle_time
                time.sleep(idle_time / 1000)

            # calculate waiting time
            arrav_val = value[0]
            self.waiting_time[value[1] - 1] += (self.current_time - arrav_val)

            if int(value[2]) != 0:
                self.gantt.append(
                    (value[1], self.current_time, self.current_time + int(value[2])))  # (p_id, start_time, end_time)
                self.current_time += value[2]  # update current time after running first job

            time.sleep(value[2] / 1000)  # time to run process

            if value[3] == "cpu_1":  # add cpu_burst2
                p = self.search(value[1])
                self.tmp_queue.append((self.current_time + p.io_time, value[1], p.cpu_burst2, "cpu_2"))

        print("gantt : p_id", "start time", "end_time", sep="\t")
        print(self.gantt)
        print(f'total time : {self.current_time}')

    def avg_turnaround_time(self):
        for pid in range(len(self.process_list)):
            process = self.search(pid + 1)

            for i in range(len(self.gantt) - 1, -1, -1):
                if (pid + 1) == self.gantt[i][0]:
                    p_end_time_in_cpu = self.gantt[i][2]
                    p_end_time = p_end_time_in_cpu
                    if process.cpu_burst2 == 0:
                        p_end_time += process.io_time
                    break
            self.turnaround_time.append(p_end_time - process.arrival_time)
            self.pid_turn_time.append((process.p_id, p_end_time - process.arrival_time))

        print(f'turn around time : {self.pid_turn_time}')
        avg = sum(self.turnaround_time) / len(self.turnaround_time)
        print(f'avg turn around time : {avg}')
        return avg

    def throughput(self):
        thrput = len(self.process_list) * 1000 / self.current_time
        print(f'throughput : {thrput}')
        return thrput

    def cpu_utilization(self):
        idle = 0
        for i in range(len(self.gantt) - 1):
            idle += self.gantt[i + 1][1] - self.gantt[i][2]

        res = (self.current_time - idle) * 100 / self.current_time
        print(f'cpu utilization : {res}%')
        return res

    def avg_response_time(self):
        for pid in range(len(self.process_list)):
            process = self.search(pid + 1)

            for i in range(len(self.gantt)):
                if (pid + 1) == self.gantt[i][0]:
                    self.response_time.append(self.gantt[i][1] - process.arrival_time)
                    self.pid_response_time.append((process.p_id, self.gantt[i][1] - process.arrival_time))
                    break

        print(f'response time : {self.pid_response_time}')
        avg = sum(self.response_time) / len(self.response_time)
        print(f'avg response time : {avg}')
        return avg

    def avg_waiting_time(self):
        print(f'waiting time : {self.waiting_time}')
        avg = sum(self.waiting_time) / len(self.waiting_time)
        print(f'avg waiting time : {avg}')
        return avg
