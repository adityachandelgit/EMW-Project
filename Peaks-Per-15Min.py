import csv
from datetime import datetime as dt


def get_peaks_per_15min(path):
    # range_15min = ['4:00 to 4:15' '4:15 to 4:30', '4:30 to 4:45', '4:45 to 5:00', '5:00 to 5:15', '5:15 to 5:30', '5:30 to 5:45', '5:45 to 6:00']

    range_15min = [[dt.strptime('16:00:00', '%H:%M:%S'), dt.strptime('16:14:59', '%H:%M:%S')],
                   [dt.strptime('16:15:00', '%H:%M:%S'), dt.strptime('16:29:59', '%H:%M:%S')],
                   [dt.strptime('16:30:00', '%H:%M:%S'), dt.strptime('16:44:59', '%H:%M:%S')],
                   [dt.strptime('16:45:00', '%H:%M:%S'), dt.strptime('16:59:59', '%H:%M:%S')],
                   [dt.strptime('17:00:00', '%H:%M:%S'), dt.strptime('17:14:59', '%H:%M:%S')],
                   [dt.strptime('17:15:00', '%H:%M:%S'), dt.strptime('17:29:59', '%H:%M:%S')],
                   [dt.strptime('17:30:00', '%H:%M:%S'), dt.strptime('17:44:59', '%H:%M:%S')],
                   [dt.strptime('17:45:00', '%H:%M:%S'), dt.strptime('18:00:00', '%H:%M:%S')]]

    with open(path) as infile:
        op = []
        reader = csv.reader(infile)
        device = ''
        year = ''
        times = [0] * 8

        for row in reader:
            device = row[0]
            year = row[1]
            infile.seek(0)
            break

        for row in reader:
            if device == row[0]:
                datetime_object = dt.strptime(row[2], '%H:%M:%S')
                for i in range(8):
                    if range_15min[i][0] <= datetime_object <= range_15min[i][1]:
                        times[i] += 1
                        continue
            else:
                for i in range(8):
                    op.append([device, year, range_15min[i][0].strftime("%H:%M:%S") + ' to ' + range_15min[i][1].strftime("%H:%M:%S"), times[i]])
                device = row[0]
                year = row[1]
                times = [0] * 8
                datetime_object = dt.strptime(row[2], '%H:%M:%S')
                for i in range(8):
                    if range_15min[i][0] <= datetime_object <= range_15min[i][1]:
                        times[i] += 1

        with open("D:/Temp/Meta-CM_Rocket-15Min.csv", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(op)


get_peaks_per_15min('C:\My-Files\SnD\USU\EMW-Research\Empatica Data\CM Rocket\Meta-CM_Rocket.csv')
