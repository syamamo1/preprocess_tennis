import os

# Documentation: https://ffmpeg.org/ffmpeg.html
def cut_video(source_video, start, end, out_path):
    in_path = f'-i {source_video}' # Input video
    duration = f'-ss {start} -to {end}' # Time range
    fps = '-r 30' # FPS
    codec = '-c copy' # Faster
    loglevel = '-loglevel fatal' # Show only fatal errors
    stats = '-stats' # Print progress/stats
    scale = 'scale=224:224' # Scale

    com = f'ffmpeg {loglevel} {stats} {duration} {scale} {in_path} {codec} {fps} {out_path}'
    os.system(com)

def fill_blank_frames(source_video):
    None
