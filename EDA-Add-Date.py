import csv
import time
import os
from datetime import datetime, timedelta
import itertools


def add_time():
    for subdir, dirs, files in os.walk('C:\My-Files\SnD\USU\EMW-Research\Empatica Data\Cache Rocket\By Date'):
        for f in files:
            if f == 'EDA.csv':
                with open(os.path.join(subdir, f), 'rb') as infile, open(os.path.join(subdir, 'With-Time-' + f), "wb") as outfile:
                    reader = csv.reader(infile)
                    initial_utc = float(next(reader)[0])
                    next(reader)

                    writer = csv.writer(outfile)
                    every4sec = 0
                    for row in reader:
                        if every4sec == 4:
                            every4sec = 0
                            initial_utc += 1
                        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(initial_utc)), row[0]])
                        every4sec += 1


def six_sec_slots():
    for subdir, dirs, files in os.walk('C:\My-Files\SnD\USU\EMW-Research\Empatica Data\Cache Rocket\By Date'):
        for f in files:
            if f == 'With-Time-EDA.csv':
                with open(os.path.join(subdir, f), 'rb') as infile, open(os.path.join(subdir, '5-Sec-Slots-' + f), "wb") as outfile:
                    reader = csv.reader(infile)
                    writer = csv.writer(outfile)
                    eda = []
                    timestamp = []
                    for row in reader:
                        timestamp.append(row[0])
                        eda.append(float(row[1]))
                        if len(eda) == 20:
                            writer.writerow([timestamp[0], format(sum(eda) / float(len(eda)), '.5f')])
                            del eda[:]
                            del timestamp[:]


def fix_artifact_timestamp():
    for subdir, dirs, files in os.walk('C:\My-Files\SnD\USU\EMW-Research\Empatica Data\Cache Rocket\By Date'):
        for f in files:
            if f[-10:] == 'Binary.csv':
                with open(os.path.join(subdir, f), 'rb') as infile, open(os.path.join(subdir, f[:len(f) - 4] + '-Fixed.csv'), "wb") as outfile:
                    reader = csv.reader(infile)
                    writer = csv.writer(outfile)
                    writer.writerow(next(reader))
                    for row in reader:
                        writer.writerow([
                            row[0],
                            datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') - timedelta(hours=6),
                            datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S') - timedelta(hours=6),
                            row[3]
                        ])


def combine_peak_artifact_csv():
    two = []
    for subdir, dirs, files in os.walk('C:\My-Files\SnD\USU\EMW-Research\Empatica Data\Cache Rocket\By Date'):
        for f in files:
            if f[-9:] == 'Fixed.csv' or f[:5] == '5-Sec':
                two.append(os.path.join(subdir, f))
                if len(two) == 2:
                    with open(two[0], 'rb') as infile1, open(two[1], 'rb') as infile2, open(os.path.join(subdir, 'Merged-EDA.csv'), "wb") as outfile:
                        reader1 = csv.reader(infile1)
                        reader2 = csv.reader(infile2)
                        next(reader1)
                        writer = csv.writer(outfile)
                        for lhs, rhs in itertools.izip(reader1, reader2):
                            rhs.append(lhs[3])
                            writer.writerow(rhs)
                        del two[:]


combine_peak_artifact_csv()
# fix_artifact_timestamp()
# six_sec_slots()
# add_time()
