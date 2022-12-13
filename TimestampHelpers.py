import pandas as pd

# Find difference between two times
# 30 fps
# t - sub
# outputs in decimal form (frames in decimals)
def subtract_timestamps(t, sub):
    # time since new_start
    # e.g. '01:20:46:11'
    # Output: 01:20:46.367

    # frames
    last2digits = int(t[-2:]) - int(sub[-2:])
    carry1 = False
    if last2digits < 0: 
        carry1 = True
        last2digits = 30 + last2digits
    third = int(1000*last2digits/30)
    
    # seconds
    second = int(t[6:8]) - int(sub[6:8])
    if carry1: second -= 1
    carry2 = False
    if second < 0: 
        carry2 = True
        second = 60 + second

    # minutes
    first = int(t[3:5]) - int(sub[3:5])
    if carry2: first -= 1
    carry3 = False
    if first < 0:
        carry3 = True

    # hours
    zero = int(t[0:2]) - int(sub[0:2])
    if carry3: zero -= 1
    
    if zero < 10:
        zero = '0' + str(zero)
    if first < 10:
        first = '0' + str(first)
    if second < 10:
        second = '0' + str(second)
    difference = f'00:{first}:{second}.{third}'
    return difference


# Outputs in decimal form
# frames in decimals
def add_timestamps(t1, t2):

    # frames
    last2digits = int(t2[-2:]) + int(t1[-2:])
    carry1 = False
    if last2digits >= 30: 
        carry1 = True
        last2digits = last2digits - 30
    third = int(1000*last2digits/30)
    
    # seconds
    second = int(t2[6:8]) + int(t1[6:8])
    if carry1: second += 1
    carry2 = False
    if second >= 60: 
        carry2 = True
        second = second - 60

    # minutes
    first = int(t2[3:5]) + int(t1[3:5])
    if carry2: first += 1
    carry3 = False
    if first >= 60:
        carry3 = True
        first = first - 60

    # hours
    zero = int(t2[0:2]) + int(t1[0:2])
    if carry3: zero += 1
    
    # pad values to be 2 digits
    if zero < 10:
        zero = '0' + str(zero)
    if first < 10:
        first = '0' + str(first)
    if second < 10:
        second = '0' + str(second)
    sum_time = f'00:{first}:{second}.{third}'
    return sum_time

# True if t1 < t2 (t2 is after)
# timestamps in frames
def compare_timestamps(t1, t2):
    t1_hours, t2_hours = int(t1[0:2]), int(t2[0:2])
    if t1_hours < t2_hours: return True
    if t1_hours > t2_hours: return False

    t1_mins, t2_mins = int(t1[3:5]), int(t2[3:5])
    if t1_mins < t2_mins: return True
    if t1_mins > t2_mins: return False

    t1_secs, t2_secs = int(t1[6:8]), int(t2[6:8])
    if t1_secs < t2_secs: return True
    if t1_secs > t2_secs: return False

    t1_frames, t2_frames = int(t1[9:11]), int(t2[9:11])
    if t1_frames < t2_frames: return True
    if t1_frames > t2_frames: return False

    elif (t1_hours == t2_hours) and (t1_mins==t2_mins):
        if (t1_secs==t2_secs) and (t1_frames==t2_frames): 
            return False # EQUAL CASE
    else: 
        print('ERROR comparing timestamps:', t1, t2)
        exit(1)

# Premiere to ffmpeg timestamps
# '01:20:46:10' -> '01:20:46.333'
def frames_to_dec(timestamp):
    last2 = int(timestamp[-2:])
    frac = int(1000*last2/30)
    return f'{timestamp[:-3]}.{frac}'

# decimal ts to frame ts
def dec_to_frames(timestamp):
    non_ms = timestamp.split('.')[0]
    ms = int(timestamp.split('.')[-1])
    frames = str(int(ms*30/1000))
    if len(frames) == 1:
        frames = f'0{frames}'
    return f'{non_ms}:{frames}'

# gets sec.ms of a timestamp
# that's already in decimal form
def to_sec_ms(timestamp):
    sec_ms = int(timestamp[6:8]) + int(timestamp.split('.')[-1])/1000
    return sec_ms

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



