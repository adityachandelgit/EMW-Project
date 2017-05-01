import csv
import itertools
import os
import time
from datetime import datetime, timedelta

path = 'D:\EMW-TPI\\Test'


def add_time():
    """Adds timestamp to EDA.csv file downloaded from Empatica.com
       Input: Path to the root directory containing EDA.csv file
       Output: A csv named 'With-Time-EDA.csv', containing the columns: Eda value and timestamp
     """
    for subdir, dirs, files in os.walk(path):
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
    """Original EDA.csv file created by empatica contains EDA entry 4 times per second. This function takes mean of 5 seconds of eda 
       values (4x5) and stores them in a new csv file
       Input: Path to the root directory containing With-Time-EDA.csv file
       Output: A csv named '5-Sec-Slots-With-Time-EDA.csv', containing 5 second EDA values
    """
    for subdir, dirs, files in os.walk(path):
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
    """Timestamp of EDA files created by empatica device is about 6 hours off. fix_artifact_timestamp() fixes this.
        Input: Path to the root directory containing un-fixed EDA file
        Output: A csv file named 'EDA-Fixed.csv'.
    """
    for subdir, dirs, files in os.walk(path):
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
    """ Combines 'Fixed timestamp' file and '5 seconds slot' file.
        Input: Path to the root directory containing Fixed timestamp' file and '5 seconds slot' file.
        Output: A csv file named 'Merged-EDA.csv'.
    """
    two = []
    for subdir, dirs, files in os.walk(path):
        for f in files:
            if f[-9:] == 'Fixed.csv' or f[:5] == '5-Sec':
                two.append(os.path.join(subdir, f))
                two.sort()
                if len(two) == 2:
                    print 'Current File 1: ' + two[0]
                    print 'Current File 2: ' + two[1]
                    with open(two[0], 'rb') as infile1, open(two[1], 'rb') as infile2, open(os.path.join(subdir, 'Merged-EDA.csv'), "wb") as outfile:
                        reader1 = csv.reader(infile1)
                        reader2 = csv.reader(infile2)
                        next(reader1)
                        writer = csv.writer(outfile)
                        for lhs, rhs in itertools.izip(reader1, reader2):
                            rhs.append(lhs[3])
                            writer.writerow(rhs)
                        del two[:]



# add_time()
# six_sec_slots()
# fix_artifact_timestamp()
# combine_peak_artifact_csv()
