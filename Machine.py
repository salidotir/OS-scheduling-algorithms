import pandas


class Process:
    def __init__(self, p_id, arrival_time, cpu_burst1, io_time, cpu_burst2):
        self.p_id = p_id
        self.arrival_time = arrival_time
        self.cpu_burst1 = cpu_burst1
        self.io_time = io_time
        self.cpu_burst2 = cpu_burst2

    def __str__(self: 'Process'):
        return '\t'.join(map(str, [self.p_id, self.arrival_time, self.cpu_burst1, self.io_time, self.cpu_burst2]))


def process_generator(n: int) -> list:
    process_list = []
    for i in range(1, n):
        df = pandas.read_csv('input.csv', skiprows=[x for x in range(1, n) if x != i])
        p_id = df['p_id'][0]
        arrival_time = df['arrival_time'][0]
        cpu_burst1 = df['cpu_burst1'][0]
        io_time = df['io_time'][0]
        cpu_burst2 = df['cpu_burst2'][0]

        process = Process(p_id, arrival_time, cpu_burst1, io_time, cpu_burst2)

        process_list.append(process)

    return process_list
