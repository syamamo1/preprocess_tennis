import cv2
import os
import pandas as pd

from TimestampHelpers import subtract_timestamps, add_timestamps, compare_timestamps
from TimestampHelpers import to_sec_ms
from VideoHelpers import miniclips, cut_video


# Sorts in/out timestamps into array, also finds which is first
def sort_timestamps(excel_sheet, in_sheet, out_sheet) -> tuple(str, list):
    in_ts = pd.read_excel(excel_sheet, sheet_name=in_sheet)
    out_ts = pd.read_excel(excel_sheet, sheet_name=out_sheet)
    in_s, in_e = in_ts.loc[:, 'start'], in_ts.loc[:, 'end']
    out_s, out_e = out_ts.loc[:, 'start'], out_ts.loc[:, 'end']

    first_label = 1
    timestamps = []
    if compare_timestamps(out_s.iloc[0], in_s.iloc[0]):
        timestamps.append(out_s.iloc[0])
        first_label = 0
    for t1, t2 in zip(in_ts.loc[:, 'start'], in_ts.loc[:, 'end']):
        timestamps.append(t1)
        timestamps.append(t2)
    if compare_timestamps(in_e.iloc[-1], out_e.iloc[-1]):
        timestamps.append(out_e.iloc[-1])

    return first_label, timestamps

# creates t-second uniform videos based on timestamps
def create_uniform_times(t, excel_sheet, in_sheet, out_sheet):
    # create 3s interval timestamps
    first_label, sorted_timestamps = sort_timestamps(excel_sheet, in_sheet, out_sheet)
    label = first_label

    timestamps = []
    labels = []
    ts_idx = 1
    my_prev = sorted_timestamps[ts_idx-1] # 1st timestamp
    stop_ts = sorted_timestamps[ts_idx] # 2nd timestamp
    my_time = add_timestamps(sorted_timestamps[0], t)
    temp_label = None
    while compare_timestamps(my_time, sorted_timestamps[-1]):
        dif = subtract_timestamps(stop_ts, my_time)
        sec_ms = to_sec_ms(dif)

        if label == 1: # handling too big cases
            if 1 < sec_ms: temp_label = 1
        elif label == 0:
            if 2 < sec_ms: temp_label = 0 

        # iterate to next timestamp
        # stops when my_time > stop_ts
        while compare_timestamps(my_time, stop_ts):
            timestamps.append((my_prev, my_time))
            if temp_label is not None: 
                labels.append(temp_label)
                temp_label = None
            else: labels.append(label)

            my_prev = my_time
            my_time = add_timestamps(my_time, t)

        # next timestamps
        stop_ts = sorted_timestamps[ts_idx]
        ts_idx += 1
    return timestamps, labels

# t-second videos for start/stop excel_sheet
def create_uniform(t, source_video, excel_sheet, out_folder):
    uniform_data = {}
    uniform_data['filename'] = []
    uniform_data['timestamp'] = []
    uniform_data['label'] = []
    # Iterate sheets (right now 6 videos)
    for i in range(6):
        in_sheet = 2*i+1 # sheet number
        out_sheet = 2*i+2
        timestamps, labels = create_uniform_times(t, excel_sheet, in_sheet, out_sheet)
        for n, (ts, l) in enumerate(zip(timestamps, labels)):
            if n == 0: temp = ts; continue
            filename = f'{t}s_{in_sheet}_{l}.mp4'
            out_path = os.path.join(out_folder, filename)
            cut_video(source_video, temp, ts, out_path)

            uniform_data['filename'].append(filename)
            uniform_data['timestamp'].append(ts)
            uniform_data['label'].append(l)

    # save timestamp/labels
    df = pd.DataFrame(uniform_data)
    df_out = os.path.join(out_folder, 'uniform_timestamps.csv')
    df.to_csv(df_out)

############### RUN YO SH-
t = '00:00:03:00'
source_video = os.path.join('dataset', 'source_videos', 'roger_corrected.mp4')
excel_sheet = os.path.join('dataset', 'timestamps.xlsx')
out_folder = os.path.join('dataset', 'uniform_dataset')

create_uniform(t, source_video, excel_sheet, out_folder)