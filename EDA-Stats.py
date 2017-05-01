import os
import csv
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np

root = 'D:\\1.Work\USU\EMW-Research\Empatica Data\CM Rocket\Cache Rocket (Backup)\By Date'


def standard_deviation_each_device():
    with open("std-dev-by-device.csv", "wb") as f:
        writer = csv.writer(f)
        for deviceId in os.listdir(root):
            for date in os.listdir(root + '/' + deviceId):
                eda = list(csv.reader(open(root + '/' + deviceId + '/' + date + '/' + 'EDA.csv', 'rb')))
                eda = eda[5:len(eda)]
                eda_float = [float(i[0]) for i in eda]
                data = [deviceId, date[:10], str(round(stats.stdev(eda_float), 3))]
                writer.writerow(data)


def raw_data():
    all_data = []
    with open("raw.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'DeviceID', 'EDA'])
        for subdir, dirs, files in os.walk('E:\\1.SnD\\Studies\\ITLS-EMW\\Rocket E4'):
            for file in files:
                if file == 'EDA.csv':
                    eda = list(csv.reader(open(os.path.join(subdir, file), 'rb')))
                    eda = eda[5:len(eda)]
                    eda_float = [float(i[0]) for i in eda]
                    subdir_split = subdir.split('\\')
                    for e in eda:
                        # writer.writerow([subdir_split[5], subdir_split[6][-6:], float(e[0])])
                        all_data.append([subdir_split[-1][-6:], subdir_split[-2], float(e[0])])
    devices = set([a[0] for a in all_data])
    data_for_a_device = []
    data_for_all_device = []
    for device in devices:
        del data_for_a_device[:]
        for data in all_data:
            if data[0] == device:
                data_for_a_device.append(float(data[2]))
        # plt.boxplot(data_for_a_device)
        # plt.title(device + ' : Lantern')
        # plt.savefig(device + '.png')
        # plt.close()
        data_for_all_device.append([a for a in data_for_a_device])
    plt.boxplot(data_for_all_device)
    plt.savefig('box.png')
    plt.close()


def all_stats():
    with open("all-stats.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerow(
            ['Date', 'DeviceID', 'Mean', 'Median', 'Std Deviation', 'Variance', 'Mode', 'Minimum', 'Maximum'])
        for subdir, dirs, files in os.walk('E:\\1.SnD\\Studies\\ITLS-EMW\\Rocket E4'):
            for file in files:
                if file == 'EDA.csv':
                    eda = list(csv.reader(open(os.path.join(subdir, file), 'rb')))
                    eda = eda[5:len(eda)]
                    eda_float = [float(i[0]) for i in eda]
                    subdir_split = subdir.split('\\')
                    current_stat = [subdir_split[5],
                                    subdir_split[6][-6:],
                                    str(stats.mean(eda_float)),
                                    str(stats.median(eda_float)),
                                    str(stats.stdev(eda_float)),
                                    str(stats.variance(eda_float)),
                                    str(stats.mode(eda_float)),
                                    str(min(eda_float)),
                                    str(max(eda_float))]
                    print current_stat
                    writer.writerow(current_stat)


# standard_deviation_each_device()
# all_stats()
raw_data()
