from FCFS import FCFS
from SJF import SJF
from RR import RR
from SRT import SRT
from Machine import *
import matplotlib.pyplot as plt
import threading
import time


def run_fcfs():
    t1 = time.time()
    fcfs = FCFS(p)
    fcfs.run()
    t2 = time.time()
    print((t2 - t1) * 1000)
    fcfs.avg_waiting_time()
    fcfs.avg_response_time()
    fcfs.avg_turnaround_time()
    fcfs.throughput()
    fcfs.cpu_utilization()

    lst = []
    for i in range(1, n):
        lst.append(process_gantt(fcfs.gantt, i))
    xlim = fcfs.gantt[len(fcfs.gantt) - 1][2]  # end of cpu processing
    plot(lst, n-1, xlim, (n-1) * 10, 'fcfs')


def run_sjf():
    t1 = time.time()
    sjf = SJF(p)
    sjf.run()
    t2 = time.time()
    print((t2 - t1) * 1000)
    sjf.avg_waiting_time()
    sjf.avg_response_time()
    sjf.avg_turnaround_time()
    sjf.throughput()
    sjf.cpu_utilization()

    lst = []
    for i in range(1, n):
        lst.append(process_gantt(sjf.gantt, i))
    xlim = sjf.gantt[len(sjf.gantt) - 1][2]  # end of cpu processing
    plot(lst, n-1, xlim, (n-1) * 10, 'sjf')


def run_rr():
    t1 = time.time()
    rr = RR(p)
    rr.run()
    t2 = time.time()
    print((t2 - t1) * 1000)
    rr.avg_waiting_time()
    rr.avg_response_time()
    rr.avg_turnaround_time()
    rr.throughput()
    rr.cpu_utilization()

    lst = []
    for i in range(1, n):
        lst.append(process_gantt(rr.gantt, i))
    xlim = rr.gantt[len(rr.gantt) - 1][2]  # end of cpu processing
    plot(lst, n-1, xlim, (n-1) * 10, 'rr')


def run_srt():
    t1 = time.time()
    srt = SRT(p)
    srt.run()
    t2 = time.time()
    print((t2 - t1) * 1000)
    srt.avg_waiting_time()
    srt.avg_response_time()
    srt.avg_turnaround_time()
    srt.throughput()
    srt.cpu_utilization()

    lst = []
    for i in range(1, n):
        lst.append(process_gantt(srt.gantt, i))
    xlim = srt.gantt[len(srt.gantt) - 1][2]  # end of cpu processing
    plot(lst, n-1, xlim, (n-1) * 10, 'srt')

def process_gantt(gantt, pid):
    new_gantt = []
    for i in range(len(gantt)):
        if gantt[i][0] == pid:
            new_gantt.append((gantt[i][1], gantt[i][2] - gantt[i][1]))
    return new_gantt


def plot(lst, n, xlim, ylim, called_func):
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, ylim)

    # Setting X-axis limits
    gnt.set_xlim(0, xlim)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time(milli second)')
    gnt.set_ylabel('Process identifier')

    yticks = [i+5 for i in range(0, n*10, 10)]
    # Setting ticks on y-axis
    gnt.set_yticks(yticks)
    # # Labelling tickes of y-axis
    gnt.set_yticklabels([f'p{i}' for i in range(1, n+1)])

    xticks = [i for i in range(0, xlim+1)]
    plt.xticks(xticks, xticks)

    # Setting graph attribute
    gnt.grid(True)

    for i in range(0, n):
        gnt.broken_barh(lst[i], (yticks[i]-5, 10), facecolors=('tab:blue'))

    plt.savefig(f'{called_func}_gantt.png')


if __name__ == '__main__':
    n = 4

    p = process_generator(n)

    fcfs_thread = threading.Thread(target=run_fcfs())

    sjf_thread = threading.Thread(target=run_sjf())

    srt_thraed = threading.Thread(target=run_srt())

    rr_thread = threading.Thread(target=run_rr())

    fcfs_thread.start()
    sjf_thread.start()
    srt_thraed.start()
    rr_thread.start()

    fcfs_thread.join()
    sjf_thread.join()
    srt_thraed.join()
    rr_thread.join()
