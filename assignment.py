import os

os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

def build_graduation_video():
    offsets = {
        "camera1_front_left.mp4": 0,
        "camera3_wide_back.mp4": 8,
        "camera4_side_angle.mp4": 18,
        "camera2_front_right.mp4": 57
    }

    cameras = {
        "camera1_front_left.mp4": VideoFileClip("starter-pack/camera1_front_left.mp4"),
        "camera3_wide_back.mp4": VideoFileClip("starter-pack/camera3_wide_back.mp4"),
        "camera4_side_angle.mp4": VideoFileClip("starter-pack/camera4_side_angle.mp4"),
        "camera2_front_right.mp4": VideoFileClip("starter-pack/camera2_front_right.mp4")
    }

    main_audio = cameras["camera1_front_left.mp4"].audio

    edl = [
        {"start": 0,  "end": 10, "cam": "camera1_front_left.mp4",  "action": "fadein",    "text": "title"},
        {"start": 10, "end": 25, "cam": "camera3_wide_back.mp4",   "action": "cut",       "text": None},
        {"start": 25, "end": 40, "cam": "camera4_side_angle.mp4",  "action": "crossfade", "text": None},
        {"start": 40, "end": 58, "cam": "camera1_front_left.mp4",  "action": "cut",       "text": "subtitle"},
        {"start": 58, "end": 65, "cam": "camera2_front_right.mp4", "action": "cut",       "text": None},
        {"start": 65, "end": 75, "cam": "camera3_wide_back.mp4",   "action": "fadeout",   "text": "credit"}
    ]

    processed_clips = []

    for item in edl:
        cam_name = item["cam"]
        master_start = item["start"]
        master_end = item["end"]
        
        local_start = master_start - offsets[cam_name]
        local_end = master_end - offsets[cam_name]
        
        clip = cameras[cam_name].subclip(local_start, local_end).without_audio()
        
        processed_clips.append(clip)

if __name__ == "__main__":
    build_graduation_video()