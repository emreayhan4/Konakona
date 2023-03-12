import os
import random
import subprocess

from twitter import *


consumer_key = "471x7CUux3kzBZOg"
consumer_secret = "Oei0u4QsYgsopFyRLroLGaxaUfFF1wBOFHMqcWq220Twd2"
token = "1613156780732809218-4KEhjC7sjEc2qqGwiiurOSQ6uUL"
token_secret = "N96s8HpzNQpJPdJEgdzDy73wWULrje98cv5gK6nkr"


def get_random_filepath():
    directory = '/Users/emreayhan/Desktop/test'
    file_ending = ('.webm')

    file_list = os.listdir(directory)
    old_file_list = list(
        filter(lambda x: not x.endswith(file_ending), file_list))
    new_file_list = list(filter(lambda x: x.endswith(file_ending), file_list))

    random_file = random.choice(new_file_list)
    random_filepath = os.path.join((directory), random_file)

    return random_filepath


def get_file_length(filepath):
    script = [
        'ffprobe',
        '-i', filepath,
        '-show_entries', 'format=duration',
        '-v', 'quiet',
        '-of', 'csv=%s' % 'p=0'
    ]

    duration = subprocess.check_output(script)
    random_time = random.uniform(0.00, float(duration))

    return float(duration)


def generate_screenshot_local(filepath, duration):
    image_count = 5
    seconds_apart = 2
    random_time = random.uniform(0.00, duration - seconds_apart * image_count)
    output_name_list = ('out_0.png', 'out_1.png', 'out_2.png', 'out_3.png')

    if image_count >= 5:
        image_count = random.randint(1, 4)

    for i in range(image_count):
        script = [
            'ffmpeg', '-y',
            '-ss', str(random_time),
            '-i', filepath,
            '-vframes', '1',
            '-vf', 'scale=1920:-1',
            '-q:v', '1',
            '-qmin', '1',
            output_name_list[i]
        ]

        random_time += seconds_apart
        subprocess.call(script)

    return output_name_list


def generate_clip_local(filepath, duration):
    clip_count = 4
    seconds_apart = 0
    clip_length = 5
    calc = seconds_apart * clip_count + float(clip_length) * clip_count
    random_time = random.uniform(0.00, duration - calc)
    output_video_list = ('out_0.mp4', 'out_1.mp4', 'out_2.mp4', 'out_3.mp4')

    for i in range(clip_count):
        script = [
            'ffmpeg', '-y',
            '-ss', str(random_time),
            '-i', filepath,
            '-t', str(clip_length),
            '-ac', '2',
            '-sn',
            '-map_chapters', '-1',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-vf', 'scale=1280:-1',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart',
            output_video_list[i]
        ]

        random_time += clip_length + seconds_apart
        subprocess.call(script)

    return output_video_list


def check_generate_video():
    chance_video = 0

    r = random.random()
    if r <= chance_video:
        return True
    else:
        return False


def post_update(images):
    t = Twitter(
        auth=OAuth(token, token_secret, consumer_key, consumer_secret))

    with open("out_0.png", "rb") as imagefile:
        imagedata = imagefile.read()

    t_upload = Twitter(domain='upload.twitter.com',
                       auth=OAuth(token, token_secret, consumer_key, consumer_secret))

    id_img1 = t_upload.media.upload(media=imagedata)["media_id_string"]

    t.statuses.update(status="", media_id=id_img1)


if __name__ == '__main__':
    filepath = get_random_filepath()
    duration = get_file_length(filepath)

    if check_generate_video():
        clips = generate_clip_local(filepath, duration)
    images = generate_screenshot_local(filepath, duration)

    # post_update(images)
