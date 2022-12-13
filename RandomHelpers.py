import pandas as pd
import time

from TimestampHelpers import subtract_timestamps, dec_to_frames

# For logging while running many
# ffmpeg commands
def log(string):
    line = '####################'
    print(f'\n{line}')
    print(string)
    print(f'\n{line}')

# Second runtime to hr:min:sec
def calculate_runtime(runtime_secs):
    hours = int(runtime_secs/3600)
    runtime_secs -= hours*3600
    mins = int(runtime_secs/60)
    runtime_secs -= mins*60
    secs = int(runtime_secs)
    runtime = f'{hours}:{mins}:{secs}'
    return runtime

# Print stats for ffmpeg
def print_stats(start_time, video_counter):
    if video_counter == 0: return
    runtime_secs = time.time()-start_time
    runtime = calculate_runtime(runtime_secs)
    ratio = round(runtime_secs/video_counter, 2)
    print(f'\nVideo counter: {video_counter}, Runtime: {runtime}, sec/vid: {ratio}')

def fix_spenc_sid(excel_sheet):
    new_start = '01:20:46:11'
    sheet = 10
    output = {}
    output['start'] = {}
    output['end'] = {}

    df = pd.read_excel(excel_sheet, sheet_name=sheet)
    starts, ends = df.loc[:, 'start'], df.loc[:, 'end']
    for i, (start, end) in enumerate(zip(starts, ends)):
        start = subtract_timestamps(start, new_start)
        end = subtract_timestamps(end, new_start)
        start = dec_to_frames(start)
        end = dec_to_frames(end)
        output['start'][i] = start
        output['end'][i] = end

    output = pd.DataFrame(output)
    output.to_csv('updated_sid.csv')

