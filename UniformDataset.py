import os
import pandas as pd
import time

from TimestampHelpers import subtract_timestamps, add_timestamps, compare_timestamps
from TimestampHelpers import to_sec_ms, dec_to_frames, frames_to_dec, sort_timestamps
from VideoHelpers import cut_video_frames, get_source_videos, generate_new_source
from RandomHelpers import log, print_stats

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
# cuts videos to .mp4 files and
# also save csv "uniform_timestamps.csv"
def create_uniform(t, num_frames, source_videos, excel_sheet, out_folder):
    start_time = time.time()
    uniform_data = {}
    uniform_data['filename'] = []
    uniform_data['timestamp'] = []
    uniform_data['label'] = []
    # Iterate videos/sheets (right now 6 videos)
    video_counter = 0
    num_videos = len(source_videos)
    # keep_going = True # for limiting num videos..
    for i, source_video in enumerate(source_videos):
        # if not keep_going: break
        log(f'Starting: {source_video} {i+1}/{num_videos}')
        in_sheet = 2*i+1 # sheet number
        out_sheet = 2*i+2

        timestamps, labels = create_uniform_times(t, excel_sheet, in_sheet, out_sheet)
        ref_start = None
        # Iterate through timestamps and labels, cut videos
        for n, (ts, l) in enumerate(zip(timestamps, labels)):
            # if video_counter == 240: 
            #     keep_going = False
            #     break # reduce size...for testing. Remove later
            start, _ = ts # in DEC

            # Generate new source so no need to decode "up till"
            if n%5==0:
                print_stats(start_time, video_counter)
                shortened_video = generate_new_source(source_video, start, timestamps[-1][-1])
                ref_start = start

            start = subtract_timestamps(dec_to_frames(start), dec_to_frames(ref_start))
            filename = f'video{i}_{n}_{l}.mp4'
            out_path = os.path.join(out_folder, filename) 
            if cut_video_frames(shortened_video, start, num_frames, out_path) == 0:
                uniform_data['filename'].append(filename)
                uniform_data['timestamp'].append(ts)
                uniform_data['label'].append(l)
                video_counter += 1
        
        log(f'Done with: {source_video} {i+1}/{num_videos}')

    # save timestamp/labels
    df = pd.DataFrame(uniform_data)
    df_out = os.path.join(out_folder, 'uniform_timestamps.csv')
    df.to_csv(df_out)
    print(f'Total number of videos: {video_counter}')
    print(f'Videos located in: {out_folder}')


############### RUN YO SH-
if __name__ == '__main__':
    t = '00:00:02:28' # 88 frames
    num_frames = 8*11 
    source_videos = get_source_videos()

    excel_sheet = os.path.join('dataset', 'timestamps.xlsx')
    out_folder = os.path.join('dataset', 'uniform_dataset8')

    create_uniform(t, num_frames, source_videos, excel_sheet, out_folder)
    print('Finished successfully')