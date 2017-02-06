import csv
import os
import random
import shutil
from datetime import datetime
from operator import itemgetter
from os.path import join

from PIL import Image

root_path = 'C:\\My-Files\\SnD\\USU\\EMW-Research\\Aditya\\PhotoScript'


def get_date_taken(path):
    return Image.open(path)._getexif()[36867]


def write_to_csv(file_save_path, header, list_to_be_written):
    with open(os.path.join(file_save_path), "wb") as fl:
        writer = csv.writer(fl)
        writer.writerow(header)
        writer.writerows(list_to_be_written)


def rename_csvs(start_index, end_index, sub_folder, ext):
    for f in os.listdir(root_path + sub_folder):
        os.rename(join(root_path + sub_folder, f), join(root_path + sub_folder, f[start_index:end_index] + ext))


def calculate_std_dev(input_path):
    for fi in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, fi)):
            output = []
            with open(os.path.join(input_path, fi)) as f:
                next(f)
                reader = csv.reader(f)
                op_line = []
                for line in reader:
                    op_line.extend(line)
                    sd_plus_025 = float(line[4]) * 0.25
                    sd_minus_025 = float(line[4]) * -0.25
                    op_line.append(sd_plus_025)
                    op_line.append(sd_minus_025)
                    try:
                        if float(line[3]) > float(line[4]):
                            op_line.append('A')
                        elif sd_minus_025 < float(line[3]) < sd_plus_025:
                            op_line.append('U')
                        else:
                            op_line.append('')
                    except:
                        op_line.append('')
                        pass
                    output.append(op_line)
                    op_line = []
            write_to_csv(
                os.path.join(input_path + '\\OP\\', fi),
                ['', 'Time', 'Smooth', 'EDA_Dif', 'SD', 'Time2', 'SD+0.25', 'SD-0.25', 'Arousal'],
                output)


def all_aroused_and_unaroused(input_path):
    stats = []
    for fi in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, fi)):
            count_aroused = 0
            count_unaroused = 0
            with open(os.path.join(input_path, fi)) as f:
                next(f)
                reader = csv.reader(f)
                for line in reader:
                    if line[8] == 'A':
                        count_aroused += 1
                    if line[8] == 'U':
                        count_unaroused += 1
            stats.append([fi.replace('_', '-').partition('.')[0], count_aroused, count_unaroused])
    write_to_csv(input_path + '\\Stats.csv', ['Date', 'Aroused', 'Unaroused'], stats)


def equal_aroused_unaroused(input_path):
    for fi in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, fi)):
            aroused = []
            unaroused = []
            with open(os.path.join(input_path, fi)) as f:
                next(f)
                reader = csv.reader(f)
                for line in reader:
                    if line[8] == 'A':
                        aroused.append(line)
                    if line[8] == 'U':
                        unaroused.append(line)
            random.shuffle(unaroused)
            unaroused = unaroused[0:len(aroused)]
        write_to_csv(
            root_path + '\\meta\\op\\outputs\\' + fi.partition('.')[0] + '-Aroused.csv',
            ['', 'Time', 'Smooth', 'EDA_Dif', 'SD', 'Time2', 'SD+0.25', 'SD-0.25', 'Arousal'],
            aroused)
        write_to_csv(
            root_path + '\\meta\\op\\outputs\\' + fi.partition('.')[0] + '-Unaroused.csv',
            ['', 'Time', 'Smooth', 'EDA_Dif', 'SD', 'Time2', 'SD+0.25', 'SD-0.25', 'Arousal'],
            unaroused)


def photo_selection(meta_csv_path, source_photo_path, dest_photo_path):
    for file_meta in os.listdir(meta_csv_path):
        if os.path.isfile(os.path.join(meta_csv_path, file_meta)):
            datetime_meta = []
            datetime_photos = []
            file_date = file_meta.partition('-')[0]
            is_aroused = str(file_meta.partition('-')[2]).partition('.')[0]
            with open(os.path.join(meta_csv_path, file_meta)) as f:
                next(f)
                reader = csv.reader(f)
                for line in reader:
                    datetime_meta.append(datetime.strptime(line[5], '%Y-%m-%d %H:%M:%S'))
            for photo in os.listdir(source_photo_path):
                if os.path.isfile(os.path.join(source_photo_path, photo)):
                    if photo.partition('-')[0] == file_date:
                        with open(os.path.join(source_photo_path, photo)) as f1:
                            next(f1)
                            reader1 = csv.reader(f1)
                            for line1 in reader1:
                                datetime_photos.append([datetime.strptime(line1[0], '%Y:%m:%d %H:%M:%S'), line1[1] + '\\' + line1[2]])
            datetime_meta.sort()
            sorted(datetime_photos, key=itemgetter(0))
            matched_photos = []
            for m in datetime_meta:
                for p in datetime_photos:
                    if p[0] >= m:
                        matched_photos.append(p)
                        break
            for matched_photo_link in matched_photos:
                shutil.copy2(matched_photo_link[1], dest_photo_path + is_aroused + '\\' + os.path.basename(matched_photo_link[1]))


# rename_csvs(7, 17, '\\meta', '.csv')
# rename_csvs(0, 10, '\\photos', '')
# calculate_std_dev(root_path + '\\meta')
# all_aroused_and_unaroused(root_path + '\\meta\\op')
# equal_aroused_unaroused(root_path + '\\meta\\op')
photo_selection(root_path + '\\meta\\op\\outputs\\Equal Aroused-Unaroused\\',
                root_path + '\\Photos\\Meta\\',
                root_path + '\\Arousal_Photos\\')
