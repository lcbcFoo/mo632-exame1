import matplotlib.pyplot as plt
import numpy as np
import subprocess
import signal
import pickle
import time
import psutil

data = {
    'package-0': [],
    'core': [],
    'uncore': [],
    'dram': []
}

pid = int(input('Enter PID for the application to be monitored: '))

def run_monitor():
    process = subprocess.Popen(['./rapl', '-s'],
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    lines = stdout.decode('utf-8').split('\n')[-6:-2]
    for l in lines:
        measure, number = l.replace('\t', '').split(': ')
        print(measure, number)
        data[measure].append(float(number[:-1]))

finished = False
while not finished:
    finished = not psutil.pid_exists(pid)
    run_monitor()
    output = open('measurements.pkl', 'wb')
    pickle.dump(data, output)
    output.close()
    time.sleep(1)

x = np.arange(len(data['core']))

plt.plot(x, data['package-0'], label='total')
plt.plot(x, data['core'], label='core')
plt.plot(x, data['dram'], label='dram')
plt.legend()
plt.title('Energy Consumption Monitoring')
plt.xlabel('Time (seconds)')
plt.ylabel('Energy Consumption (J)')
plt.savefig('measurements-plot.png')

