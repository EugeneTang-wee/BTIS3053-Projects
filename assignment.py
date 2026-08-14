import os

# 必须在导入 moviepy 之前设置环境变量
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

def build_graduation_video():
    # 1. 记录机位偏移量 (基于 Camera 1 主时间轴)
    offsets = {
        "camera1_front_left.mp4": 0,
        "camera3_wide_back.mp4": 8,
        "camera4_side_angle.mp4": 18,
        "camera2_front_right.mp4": 57
    }

    # 2. 读取视频素材
    cameras = {
        "camera1_front_left.mp4": VideoFileClip("starter-pack/camera1_front_left.mp4"),
        "camera3_wide_back.mp4": VideoFileClip("starter-pack/camera3_wide_back.mp4"),
        "camera4_side_angle.mp4": VideoFileClip("starter-pack/camera4_side_angle.mp4"),
        "camera2_front_right.mp4": VideoFileClip("starter-pack/camera2_front_right.mp4")
    }

    # 获取主音频轨道 (Camera 1)
    main_audio = cameras["camera1_front_left.mp4"].audio

    # 3. 设计合法的 EDL (总长 75 秒，满足 60-180 秒要求，且确保机位在指定时间已录制)
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
        
        # 计算本地截取时间 (Local Time = Master Time - Offset)
        local_start = master_start - offsets[cam_name]
        local_end = master_end - offsets[cam_name]
        
        # 截取画面并移除原声，以避免音频冲突
        clip = cameras[cam_name].subclip(local_start, local_end).without_audio()
        
        # Add overlays (Title, Subtitle, Ending credit)
        if item["text"] == "title":
            txt_clip = TextClip("Kindergarten Graduation 2026", fontsize=60, color='white', font='Arial-Bold')
            txt_clip = txt_clip.set_position('center').set_duration(clip.duration)
            clip = CompositeVideoClip([clip, txt_clip])
            
        elif item["text"] == "subtitle":
            txt_clip = TextClip("Certificate Presentation", fontsize=35, color='yellow', font='Arial')
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(clip.duration)
            clip = CompositeVideoClip([clip, txt_clip])
            
        elif item["text"] == "credit":
            txt_clip = TextClip("Thank You for Watching", fontsize=50, color='white', font='Arial-Bold')
            txt_clip = txt_clip.set_position('center').set_duration(clip.duration)
            clip = CompositeVideoClip([clip, txt_clip])

        # Add transitions
        if item["action"] == "fadein":
            clip = clip.fadein(1.0)
        elif item["action"] == "fadeout":
            clip = clip.fadeout(1.0)
        elif item["action"] == "crossfade":
            clip = clip.crossfadein(1.0)

        processed_clips.append(clip)

    # 4. 拼接静音视频轨道
    final_video = concatenate_videoclips(processed_clips, method="compose")

    # 5. 提取统一的主音频轨道 (从 0 秒到 EDL 结束时间)
    final_duration = edl[-1]["end"]
    final_audio = main_audio.subclip(0, final_duration)
    
    # 将主音频设置回最终合成的视频中
    final_sequence = final_video.set_audio(final_audio)

    # 6. 导出 MP4
    output_filename = "BTIS3053_2026B_project_output.mp4"
    final_sequence.write_videofile(
        output_filename, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac",
        threads=4
    )

    # 释放内存
    for cam in cameras.values():
        cam.close()
    final_video.close()
    final_sequence.close()

if __name__ == "__main__":
    build_graduation_video()