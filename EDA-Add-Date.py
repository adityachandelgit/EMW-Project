import csv
import time
import os


for subdir, dirs, files in os.walk('C:\Users\Aditya\Desktop\Cache Rocket'):
    for file in files:
        f = open(os.path.join(subdir, file), 'rb')
        reader = csv.reader(f)

        data = []
        initial_utc = 0
        for i, row in enumerate(reader):
            if i == 0:
                initial_utc = int(float(row[0]))
                break

        ignore = -1
        for i, row in enumerate(reader):
            if i > 1:
                ignore += 1
            if ignore == 4:
                initial_utc += 1
                ignore = 0
            if i >= 4:
                d = [time.strftime('%H:%M:%S', time.localtime(initial_utc)), row[0]]
                data.append(d)

        file_op = 'OP-' + file
        with open(os.path.join(subdir, file_op), "wb") as f:
            writer = csv.writer(f)
            writer.writerows(data)


