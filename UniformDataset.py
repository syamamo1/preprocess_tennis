import os
import pandas as pd

from TimestampHelpers import subtract_timestamps, add_timestamps, compare_timestamps
from TimestampHelpers import to_sec_ms, dec_to_frames, frames_to_dec
from VideoHelpers import cut_video_frames, get_source_videos, generate_new_source

# Sorts in/out timestamps into array, also finds which is first
def sort_timestamps(excel_sheet, in_sheet, out_sheet):
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
    ts_idx = 0
    my_prev = frames_to_dec(sorted_timestamps[ts_idx]) # 1st timestamp, in DEC
    my_time = add_timestamps(sorted_timestamps[0], t) # DEC
    temp_label = None
    while compare_timestamps(my_time, sorted_timestamps[-1]):
        # next ts
        ts_idx += 1
        stop_ts = sorted_timestamps[ts_idx]
        # iterate to next timestamp, stops when my_time > stop_ts
        while compare_timestamps(dec_to_frames(my_time), stop_ts):
            timestamps.append((my_prev, my_time))
            if temp_label is not None: 
                labels.append(temp_label)
                temp_label = None
            else: labels.append(label)

            my_prev = my_time # DEC
            my_time = add_timestamps(dec_to_frames(my_time), t) # DEC

        # handling too big cases
        dif = subtract_timestamps(dec_to_frames(my_time), stop_ts)
        sec_ms = to_sec_ms(dif)
        if label == 1: # IN threshold
            if 0.5 < sec_ms: temp_label = 1
        elif label == 0: # OUT threshold
            if 2.8 < sec_ms: temp_label = 0
        label = 1 - label
    return timestamps, labels

# t-second videos for start/stop excel_sheet
def create_uniform(t, source_videos, excel_sheet, out_folder):
    uniform_data = {}
    uniform_data['filename'] = []
    uniform_data['timestamp'] = []
    uniform_data['label'] = []
    # Iterate videos/sheets (right now 6 videos)
    video_counter = 0
    for i, source_video in enumerate(source_videos):

        source_video = source_videos[i]
        in_sheet = 2*i+1 # sheet number
        out_sheet = 2*i+2
        timestamps, labels = create_uniform_times(t, excel_sheet, in_sheet, out_sheet)

        ref_start = None
        for n, (ts, l) in enumerate(zip(timestamps, labels)):
            start, end = ts # in DEC

            # Generate new source so no need to decode "up till"
            if n%5==0:
                print('\n')
                shortened_video = generate_new_source(source_video, start, timestamps[-1][-1])
                ref_start = start

            start = subtract_timestamps(dec_to_frames(start), dec_to_frames(ref_start))
            filename = f'video{i}_{n}_{l}.mp4'
            out_path = os.path.join(out_folder, filename) 
            cut_video_frames(shortened_video, start, 96, out_path)

            uniform_data['filename'].append(filename)
            uniform_data['timestamp'].append(ts)
            uniform_data['label'].append(l)
            video_counter += 1
            line = '##################################################'
            if video_counter%100==0: print(f'\n\nFinished video: {video_counter} {line}')

    # save timestamp/labels
    df = pd.DataFrame(uniform_data)
    df_out = os.path.join(out_folder, 'uniform_timestamps.csv')
    df.to_csv(df_out)
    print(f'Total number of videos: {video_counter}')
    print(f'Videos located in: {out_folder}')



############### RUN YO SH-
t = '00:00:03:09' # 96 frames
source_videos = get_source_videos()

excel_sheet = os.path.join('dataset', 'timestamps.xlsx')
out_folder = os.path.join('dataset', 'uniform_dataset')

create_uniform(t, source_videos, excel_sheet, out_folder)
print('Finished successfully')