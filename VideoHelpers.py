import os

# Documentation: https://ffmpeg.org/ffmpeg.html
def cut_video_range(source_video, start, end, out_path):
    input_s = f'-i {source_video}' # Input video
    fps = '-r 30' # FPS
    loglevel = '-loglevel fatal' # Show only fatal errors
    stats = '-stats' # Print progress/stats

    time_range = f'-ss {start} -to {end}' # Time range
    codec = '-c copy' # Faster
    
    # no scale
    com = f'ffmpeg {loglevel} {stats} {time_range} {input_s} {codec} {fps} {out_path}'
    return os.system(com) # return 0 on success

# Cut video to certain amount of frames
def cut_video_frames(source_video, start, num_frames, out_path):
    input_s = f'-i {source_video}' # Input video
    fps = '-r 30' # FPS
    loglevel = '-loglevel fatal' # Show only fatal errors
    stats = '-stats' # Print progress/stats

    num_frames = f'-frames:v {num_frames}' # 96 frames here
    scale = '-vf scale=224:224,setsar=1' # Scale, setsar (pixel aspect ratio) ,setsar=1:1

    com = f'ffmpeg {loglevel} {stats} {input_s} -ss {start} {scale} {num_frames} {fps} {out_path}'
    return os.system(com) # return 0 on success



# Generate new source video
# returns path to video
def generate_new_source(source_video, start, end):
    directory = os.path.split(source_video)[0]
    temp_name = 'temp_source.mp4'
    out_path = os.path.join(directory, temp_name)
    if os.path.exists(out_path): os.remove(out_path) # delete if exists
    cut_video_range(source_video, start, end, out_path)
    return out_path


def fill_blank_frames(source_video):
    None


# All my video filenames
def get_source_videos():
    source_videos = []
    names = ['spencer_glen.mp4','phuc_dan.mp4','andre_rh.mp4',
            'spencer_sid.mp4','spencer_sid_ending.mp4','roger_corrected.mp4']
    for filename in names:
        path = os.path.join('dataset', 'source_videos', filename)
        source_videos.append(path)
    return source_videos        