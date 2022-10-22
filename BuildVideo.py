import enum
import cv2
import numpy as np

def build_video(source, out_name, starts, ends, fps, size):
    video = cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*'h264'), fps, size)
    for i, start in enumerate(starts):
        end = ends[i]
        source.set(cv2.CAP_PROP_POS_FRAMES, start) 
        for _ in range(end-start+1):
            _, image = source.read()
            video.write(image)
    print('done with output! check it out boi')