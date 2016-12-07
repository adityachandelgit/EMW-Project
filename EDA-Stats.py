import os
import csv
import statistics as stats

root_dir = 'E:\\1.SnD\\Studies\\ITLS-EMW\\Rocket E4'

with open("all-stats.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'DeviceID', 'Mean', 'Median', 'Std Deviation', 'Variance', 'Mode', 'Minimum', 'Maximum'])
    for subdir, dirs, files in os.walk(root_dir):
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
