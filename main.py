import os.path
import random

from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


def resize_video(input_path, output_path, text):
    target_width = 1080
    target_height = 1920

    video = VideoFileClip(input_path)

    width, height = video.size
    aspect_ratio = width / height

    new_width = target_width
    new_height = int(new_width / aspect_ratio)

    black_bg = ColorClip(size=(target_width, target_height), color=[247, 55, 40])

    y_pos = (target_height - new_height) / 2

    final_clip = CompositeVideoClip([
        black_bg.set_duration(video.duration),
        video.resize((new_width, new_height)).set_position((0, y_pos)).set_duration(video.duration)
    ])

    txt_clip = TextClip(text, fontsize=75, color='black', bg_color='yellow', font='Arial')
    txt_width, _ = txt_clip.size

    speed = (new_width + txt_width) / video.duration

    if speed < 300:
        speed = 300

    start_y = random.uniform(txt_clip.h, target_height - txt_clip.h)

    txt_clip = txt_clip.set_position(('right', 'bottom')).set_duration(video.duration).set_start(0).set_end(
        video.duration).set_position(lambda t: (1000 - speed * t, start_y))

    final_clip_with_text = CompositeVideoClip([final_clip, txt_clip])

    #final_clip_with_text.write_videofile(output_path, codec='libx264', fps=video.fps)
    final_clip_with_text.write_videofile(output_path, codec='libvpx', fps=video.fps)


def get_mp4_files_in_folder(folder_path):
    mp4_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.webm')]
    return mp4_files


if __name__ == '__main__':
    source_videos = os.path.join('.', 'C:\\27_11_pasta_recipe')
    output_videos = os.path.join('.', 'C:\\27_edited')

    all_source_videos = get_mp4_files_in_folder(folder_path=source_videos)

    for video in all_source_videos:
        source_video = os.path.join(source_videos, video)
        output_video = os.path.join(output_videos, video)
        text = 'Меню в подарок и бесплатные рецепты по ссылке в комментах. Переходи скорее и забирай.'
        resize_video(input_path=source_video, output_path=output_video, text=text)
