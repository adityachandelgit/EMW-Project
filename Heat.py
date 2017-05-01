import csv
import itertools
import os
import time
from datetime import datetime, timedelta
import numpy as np

path = 'D:\\1.Work\USU\EMW-Research\Empatica Data\CM Rocket\Cache Rocket (Backup All Artifacts)\By Date'
# path = 'D:\\1.Work\USU\EMW-Research\Empatica Data\CM Lantern\Lantern\By Date'

# Rocket
devices = ['A00845', 'A00558', 'A008F2', 'A0093C', 'A00BF9', 'A00611', 'A00629', 'A009D3', 'A00938', 'A00172', 'A00775', 'A00C42']
# Lantern
# devices = ['A00558', 'A00629', 'A00BF9', 'A00938', 'A00172', 'A0093C', 'A009D3', 'A00611', 'A00803', 'A00C42', 'A00845', 'A00481', 'A008F2']


def heat(device):
    all_data = []
    for subdir, dirs, files in os.walk(path):
        for f in files:
            if f == 'With-Time-EDA.csv' and device == subdir[-6:]:
                with open(os.path.join(subdir, f), 'rb') as infile:
                    data_no_device_name = list(csv.reader(infile))

                    a_data_5min = []

                    for i in xrange(0, len(data_no_device_name), 4 * 60 * 5):
                        data_5_mins = []
                        for j in xrange(i, i + 4 * 60 * 5, 1):
                            if j < len(data_no_device_name):
                                data_5_mins.append(
                                    [data_no_device_name[j][0], round(float(data_no_device_name[j][1]), 5)])

                        if i + 4 * 60 * 5 > len(data_no_device_name):
                            a_data_5min.append([data_no_device_name[len(all_data) - 1][0],
                                                round(np.mean([float(data[1]) for data in data_5_mins]), 5),
                                                subdir[-6:]])
                        else:
                            a_data_5min.append([data_no_device_name[i + 4 * 60 * 5 - 1][0],
                                                round(np.mean([float(data[1]) for data in data_5_mins]), 5),
                                                subdir[-6:]])

                    all_data.extend(a_data_5min)

    maximum = max(float(data[1]) for data in all_data)

    all_data_normalized = []
    for dat in all_data:
        all_data_normalized.append([dat[0], round(float(dat[1]) / maximum, 5), dat[2]])

    whisker = 1 / 8.0

    data_with_heat = []

    for d in all_data_normalized:
        data = float(d[1])
        if data < whisker:
            d.append(whisker)
        elif whisker < data <= whisker * 2:
            d.append(whisker * 2)
        elif whisker * 2 < data <= whisker * 3:
            d.append(whisker * 3)
        elif whisker * 3 < data <= whisker * 4:
            d.append(whisker * 4)
        elif whisker * 4 < data <= whisker * 5:
            d.append(whisker * 5)
        elif whisker * 5 < data <= whisker * 6:
            d.append(whisker * 6)
        elif whisker * 6 < data <= whisker * 7:
            d.append(whisker * 7)
        elif whisker * 7 < data <= whisker * 8:
            d.append(whisker * 8)

        data_with_heat.append(d)

    return data_with_heat


data_all_devices = []
for device in devices:
    data_all_devices.extend(heat(device))

with open("Heat_Rocket_5Min_Intervals.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data_all_devices)
