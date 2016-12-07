import csv
import time
import datetime

f = open('EDA.csv', 'rb')
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

count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0

slot1 = 0.0
slot2 = 0.0
slot3 = 0.0
slot4 = 0.0
slot5 = 0.0
slot6 = 0.0

for line in data:
    if datetime.time(16, 0, 0) <= datetime.time(int(line[0][0:2]), int(line[0][3:5]), int(line[0][6:8])) <= datetime.time(16, 15, 0):
        count1 += 1
        slot1 += float(line[1])
    elif datetime.time(16, 15, 1) <= datetime.time(int(line[0][0:2]), int(line[0][3:5]), int(line[0][6:8])) <= datetime.time(16, 30, 0):
        count2 += 1
        slot2 += float(line[1])
    elif datetime.time(16, 30, 1) <= datetime.time(int(line[0][0:2]), int(line[0][3:5]), int(line[0][6:8])) <= datetime.time(16, 45, 0):
        count3 += 1
        slot3 += float(line[1])
    elif datetime.time(16, 45, 1) <= datetime.time(int(line[0][0:2]), int(line[0][3:5]), int(line[0][6:8])) <= datetime.time(17, 00, 0):
        count4 += 1
        slot4 += float(line[1])
    elif datetime.time(17, 00, 1) <= datetime.time(int(line[0][0:2]), int(line[0][3:5]), int(line[0][6:8])) <= datetime.time(17, 15, 0):
        count5 += 1
        slot5 += float(line[1])
    elif datetime.time(17, 15, 1) <= datetime.time(int(line[0][0:2]), int(line[0][3:5]), int(line[0][6:8])) <= datetime.time(17, 30, 0):
        count6 += 1
        slot6 += float(line[1])
    else:
        pass

meanT = (slot1 + slot2 + slot3 + slot4 + slot5 + slot6) / (count1 + count2 + count3 + count4 + count5 + count6)
mean1 = slot1 / count1
mean2 = slot2 / count2
mean3 = slot3 / count3
mean4 = slot4 / count4
mean5 = slot5 / count5
# mean6 = slot6 / count6

s1 = mean1 / meanT
s2 = mean2 / meanT
s3 = mean3 / meanT
s4 = mean4 / meanT
s5 = mean5 / meanT
# s6 = mean6 / meanT

print 'S1:', s1
print 'S2:', s2
print 'S3:', s3
print 'S4:', s4
print 'S5:', s5
# print 'S6:', s6
