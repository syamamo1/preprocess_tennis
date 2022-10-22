import cv2
from MakeDataset import unique_frames
from BuildVideo import build_video
import time
import math

def get_video_info(capture):
    fps = math.ceil(capture.get(cv2.CAP_PROP_FPS)) # get fps
    width  = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return fps, width, height

def main():
    start = time.time()
    dataset = 'dataset'
    for i in range(1, 11):
        print('Video {}'.format(i))
        edited = cv2.VideoCapture(f'{dataset}/e{i}.mp4')
        unedited = cv2.VideoCapture(f'{dataset}/ue{i}.mp4')
        fps, width, height = get_video_info(edited)

        sf, ef = unique_frames(edited, unedited, fps, (width, height))
        print(sf, ef, '\n')
    num_secs = time.time()-start
    # build_video(unedited, 'output_vids/test_output.mp4', [sf], [ef], fps, (width, height))

    print('Runtime: {} min, {} sec'.format(num_secs//60, round(num_secs%60, 1)))


if __name__ == '__main__':
    main()