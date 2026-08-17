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

if __name__ == "__main__":
    build_graduation_video()