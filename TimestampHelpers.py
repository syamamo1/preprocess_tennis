# Find difference between two times
# 30 fps
# t2 - t1
def subtract_timestamps(t1, t2):
    # time since new_start
    # e.g. '01:20:46:11'
    # Output: 01:20:46.367

    # frames
    last2digits = int(t2[-2:]) - int(t1[-2:])
    carry1 = False
    if last2digits < 0: 
        carry1 = True
        last2digits = 30 + last2digits
    third = int(1000*last2digits/30)
    
    # seconds
    second = int(t2[6:8]) - int(t1[6:8])
    if carry1: second -= 1
    carry2 = False
    if second < 0: 
        carry2 = True
        second = 60 + second

    # minutes
    first = int(t2[3:5]) - int(t1[3:5])
    if carry2: first -= 1
    carry3 = False
    if first < 0:
        carry3 = True

    # hours
    zero = int(t2[0:2]) - int(t1[0:2])
    if carry3: zero -= 1
    
    if zero < 10:
        zero = '0' + str(zero)
    if first < 10:
        first = '0' + str(first)
    if second < 10:
        second = '0' + str(second)
    difference = f'00:{first}:{second}.{third}'
    return difference


def add_timestamps(t1, t2):

    # frames
    last2digits = int(t2[-2:]) + int(t1[-2:])
    carry1 = False
    if last2digits > 30: 
        carry1 = True
        last2digits = last2digits - 30
    third = int(1000*last2digits/30)
    
    # seconds
    second = int(t2[6:8]) + int(t1[6:8])
    if carry1: second += 1
    carry2 = False
    if second > 60: 
        carry2 = True
        second = second - 60

    # minutes
    first = int(t2[3:5]) + int(t1[3:5])
    if carry2: first += 1
    carry3 = False
    if first > 60:
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
# '01:20:46:10' -> '01:20:46:33'
def convert_timestamps(timestamp):
    last2 = int(timestamp[-2:])
    frac = int(1000*last2/30)
    return f'{timestamp[:-3]}.{frac}'

# gets sec.ms of a timestamp
def to_sec_ms(timestamp):
    sec_ms = int(timestamp[6:8]) + int(timestamp.split('.')[-1])/1000
    return sec_ms

# outputs miniclips based on IN start, end
# output list of 3s timestamps and labels
# NOT FINISHED YET
# Probably useless
def miniclips(t, start, end, label):
    # e.g. '01:20:46:11'
    next_ts = add_timestamps(start, t)
    timestamps = []
    labels = []

    #
    # add start "overflow"
    
    #

    while compare_timestamps(next_ts, end): #if end is after next_ts
        timestamps.append(next_ts)
        labels.append(label)
        next_ts = add_timestamps(next_ts, t)

    # end "overflow"
    dif = subtract_timestamps(start, end)
    if int(dif[6:8]) + int(dif.split('.')[-1])/1000 > 0.3:
        label = None 
        # 
        # do something here 
    
    return timestamps, labels


