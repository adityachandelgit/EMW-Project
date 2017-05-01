import datetime
import json
import os

import subprocess32 as sp


def probe(vid_file_path):
    """ Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    """
    if type(vid_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
        return

    command = ["ffprobe",
               "-loglevel", "quiet",
               "-print_format", "json",
               "-show_format",
               "-show_streams",
               vid_file_path
               ]

    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)


def duration(vid_file_path):
    """ Video's duration in seconds, return a float number
    """
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('I found no duration')
    # return None


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def generate_subtitle(st, dur, full_path):
    op = open(full_path[:-4] + '.srt', 'w')
    current_time = datetime.datetime(1900, 1, 1, 0, 0, 0)
    for sec in list(range(1, int(dur) + 1)):
        op.write(str(sec) + '\n')
        op.write(str(current_time.strftime("%H:%M:%S,%f")) + ' --> ' + str((current_time + datetime.timedelta(seconds=1)).strftime("%H:%M:%S,%f")) + '\n')
        op.write(st.strftime("%I:%M:%S %p") + '\n\n')
        st = st + datetime.timedelta(seconds=1)
        current_time = current_time + datetime.timedelta(seconds=1)
    op.close()


for subdir, dirs, files in os.walk("G:\EMW\CM Rocket\GoPro"):
    for f in files:
        if f[-4:] == '.MP4':
            file_path = os.path.join(subdir, f)
            duration_sec = duration(file_path)
            start_time = modification_date(file_path) - datetime.timedelta(seconds=duration_sec)
            generate_subtitle(start_time, duration_sec, file_path)
