import os
import csv
import statistics as stats


root = 'C:/My-Files/SnD/USU/EMW-Research/Empatica Data/Cache Rocket/By Device'


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


standard_deviation_each_device()


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


# all_stats()
