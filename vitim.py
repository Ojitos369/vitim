"""
pip install opencv-python moviepy
"""
from moviepy.editor import VideoFileClip
import numpy as np
import os
import argparse
from datetime import timedelta

SAVING_FRAMES_PER_SECOND = 10

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")


def get_time_seconds(time):
    seconds_time = 0
    if not time:
        return seconds_time
    time = time.replace('-', ':')
    time = time.split(':')
    time = time[::-1]

    seconds_time = int(time[0])
    if len(time) > 1:
        seconds_time += int(time[1]) * 60
    if len(time) > 2:
        seconds_time += int(time[2]) * 60 * 60

    return seconds_time


def main(video_file, path_save, base_name, ext, start, end):
    
    if not video_file:
        raise Exception('Debe especificar un archivo de video (--file <video_file>)')
    base_name = base_name if base_name else "".join(video_file.split(".")[:-1])
    
    video_clip = VideoFileClip(video_file)
    
    filename, _ = os.path.splitext(video_file)
    
    if not os.path.isdir(filename) and not path_save:
        os.mkdir(filename)
    
    if path_save:
        os.system(f'mkdir -p {path_save}')
    else:
        path_save = filename
    
    if not ext:
        ext = 'png'
    
    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)

    print(f'\nvideo file: {video}\npath to save: {path_save}\nbase name: {name}\nfps: {SAVING_FRAMES_PER_SECOND} -> {saving_frames_per_second}\nextension: {ext}\n')
    saving_frames_per_second = SAVING_FRAMES_PER_SECOND
    print(f'\nvideo file: {video}\npath to save: {path_save}\nbase name: {name}\nfps: {SAVING_FRAMES_PER_SECOND} -> {saving_frames_per_second}\nextension: {ext}\n')

    # if SAVING_FRAMES_PER_SECOND is set to 0, step is 1/fps, else 1/SAVING_FRAMES_PER_SECOND
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second
    # iterate over each possible frame
    i = 0
    
    time_start = get_time_seconds(start)
    time_end = get_time_seconds(end)
    
    print(f'Start: {time_start} End: {time_end}')
    
    for current_duration in np.arange(0, video_clip.duration, step):
        # print(current_duration)
        if (current_duration < time_start):
            continue
        if current_duration > time_end > 0:
            print(f'Cerrando at {current_duration} > {time_end}')
            break
        i += 1
        # format the file name and save it
        frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration)).replace(":", "-")
        # frame_filename = os.path.join(filename, f"frame{frame_duration_formatted}.jpg")
        # exit_name = f'{base_name}-{frame_duration_formatted}.jpg'
        exit_name = f'{base_name}-{i}.{ext}'
        if path_save:
            frame_filename = os.path.join(path_save, exit_name)
        else:
            frame_filename = os.path.join(filename, exit_name)
        # save the frame with the current duration
        video_clip.save_frame(frame_filename, current_duration)
        print(f'Saving {i}: {exit_name} time {frame_duration_formatted}: ', True)
    
    # make zip file
    zip_name = f'{base_name}-{saving_frames_per_second}.zip'
    os.system(f'zip -r {zip_name} {path_save}')


if __name__ == "__main__":
    # global SAVING_FRAMES_PER_SECOND
    a = argparse.ArgumentParser()
    a.add_argument("--file", help="path to video")
    a.add_argument("--path", help="path to images")
    a.add_argument("--name", help="base name for images")
    a.add_argument("--fps", help="frames per second")
    a.add_argument("--type", help="type of image")
    a.add_argument("--start", help="time to start")
    a.add_argument("--end", help="time to end")
    
    args = a.parse_args()
    
    # print(args)
    video = args.file
    path_save = args.path
    name = args.name
    fps = args.fps
    ext = args.type
    start = args.start
    end = args.end
    if fps:
        SAVING_FRAMES_PER_SECOND = int(fps)
    main(video, path_save, name, ext, start, end)


"""
python vitim.py \
--file your_path_video.(webm,mp4,etc) \
--path path_to_save_images/ \
--name base_name_for_images \
--fps frames_per_second(30,60) \
--type image_type(png,jpg,etc) \
--start time_to_start(60,15,03:12) \
--end time_to_end(60,15,03:12)
"""
