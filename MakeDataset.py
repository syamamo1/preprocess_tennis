import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tqdm import tqdm
import time
import os

def get_video_info(capture):
    fps = math.ceil(capture.get(cv2.CAP_PROP_FPS)) # get fps
    width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, width, height

def graph_difference(sum_difs, av_difs, max_difs):
    _, axs = plt.subplots(3, sharex=True)
    xs = np.arange(len(sum_difs))
    axs[0].scatter(xs, sum_difs, label='sum difs')
    axs[1].scatter(xs, av_difs, label='av difs')
    axs[2].scatter(xs, max_difs, label='max difs')
    for ax in axs: 
        ax.legend()
        ax.grid()
    plt.show()

def unique_frames(edited, unedited, fps, size):
    '''Get indexes of start, end of edited_vid in unedited_vid '''
    num_unedited_frames = int(unedited.get(cv2.CAP_PROP_FRAME_COUNT))
    num_edited_frames = int(edited.get(cv2.CAP_PROP_FRAME_COUNT))
    start_ans = cv2.cvtColor(edited.read()[1], cv2.COLOR_BGR2GRAY)
    # pd.DataFrame(start_ans).to_csv('start_ans.csv')
    print('num frames', num_edited_frames, num_unedited_frames)
    edited.set(cv2.CAP_PROP_POS_FRAMES, num_edited_frames-1) 
    end_ans = cv2.cvtColor(edited.read()[1], cv2.COLOR_BGR2GRAY)
    
    sample_rate = 1
    sum_difs = []
    av_difs = []
    max_difs = []
    ans = start_ans
    start_frame, end_frame = None, None
    for fno in tqdm(range(0, num_unedited_frames, sample_rate), 'Searching for frame'):
        unedited.set(cv2.CAP_PROP_POS_FRAMES, fno)
        current_frame = cv2.cvtColor(unedited.read()[1], cv2.COLOR_BGR2GRAY)

        d = cv2.absdiff(current_frame, ans)
        sum_difs.append(np.sum(d))
        av_difs.append(np.average(d))
        max_dif = d.max()
        max_difs.append(max_dif)
        
        if d.max() <= 50: # same frame # 30 for e1/ue1, 27 control0/1, 
            if start_frame is None: 
                print('FOUND START', max_dif)
                # cv2.imshow('start_guess', current_frame)
                start_frame = fno
                ans = end_ans
            else: 
                print('FOUND END', max_dif)
                end_frame = fno
                # cv2.imshow('end_guess', current_frame)
                break

    # graph_difference(sum_difs, av_difs, max_difs)
    return start_frame, end_frame


def make_dataset():
    start = time.time()
    dataset = 'dataset'
    info = {}
    info['starts'] = []
    info['ends'] = []
    for i in range(1, 11):
        print('Video {}'.format(i))
        edited = cv2.VideoCapture(f'{dataset}/e{i}.mp4')
        unedited = cv2.VideoCapture(f'{dataset}/ue{i}.mp4')
        fps, width, height = get_video_info(edited)

        sf, ef = unique_frames(edited, unedited, fps, (width, height))
        info['starts'].append(sf)
        info['ends'].append(ef)
        print(sf, ef, '\n')
    num_secs = time.time()-start
    df = pd.DataFrame(info)
    df.to_csv('starts_ends.csv')

    print('Runtime: {} min, {} sec'.format(num_secs//60, round(num_secs%60, 1)))

# make_dataset()

# Premiere to ffmpeg
def convert_timestamps(timestamp):
    last2 = int(timestamp[-2:])
    frac = int(1000*last2/30)
    return f'{timestamp[:-3]}.{frac}'

def make_dataset2(source_video, timestamps, out_folder):
    # IN
    in_ts = pd.read_excel(timestamps, sheet_name='IN')
    for i, (start, end) in enumerate(zip(in_ts.loc[:, 'start'], in_ts.loc[:, 'end'])):
        start, end = convert_timestamps(start), convert_timestamps(end)
        outfile = os.path.join(out_folder, 'ins', f'in{i}.mp4')
        com = f'ffmpeg -i {source_video} -ss {start} -to {end} {outfile}'
        os.system(com)

    # OUT
    out_ts = pd.read_excel(timestamps, sheet_name='OUT')
    for i, (start, end) in enumerate(zip(out_ts.loc[:, 'start'], out_ts.loc[:, 'end'])):
        start, end = convert_timestamps(start), convert_timestamps(end)
        outfile = os.path.join(out_folder, 'outs', f'out{i}.mp4')
        com = f'ffmpeg -i {source_video} -ss {start} -to {end} {outfile}'
        os.system(com)


source_video = os.path.join('source_videos', 'spencer_sid.mp4')
make_dataset2(source_video, 'timestamps.xlsx', 'sid_dataset')