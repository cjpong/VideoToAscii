import cv2
from PIL import Image
import time
import os
from playsound import playsound
from moviepy.editor import *

#ascii_chars = ["@", "#", "%", "E", "?", "+", "*", ";", ":", ",", " "]
ascii_chars = [" ", ",", ":", ";", "*", "+", "?", "E", "%", "#", "@"]

ascii_frames = []

def video_to_frames(video):
    # ascii_frames = []
    dir = 'frames'
    vidcap = cv2.VideoCapture(video)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    success, image = vidcap.read()
    height, width, channels = image.shape
    aspect_ratio = height/width
    count = 0
    while success:
        cv2.imwrite("frames\%d.jpg" % count, image)
        success, image = vidcap.read()
        print('frame ', count, ' extracted')
        frames_to_ascii("frames\%d.jpg" % count, aspect_ratio)
        os.remove("frames\%d.jpg" % count)
        count += 1
    video2 = VideoFileClip(os.path.join(video))
    if video2.audio is not None:
        sound = video.replace("mp4", "mp3")
        video2.audio.write_audiofile(os.path.join(sound))
    savevid = input("would you like to save this video?(y/n)")
    if savevid == "y":
        savepath = input("what folder would you like to save to? Please put the full directory here: \n")
        filename = savepath + "\\" + video[video.rfind('\\'):].replace("mp4", "txt")
        print(filename)
        if video2.audio is not None:
            soundname = sound[sound.rfind('\\'):]
            newsound = f"{savepath}\\{soundname}"
            os.rename(sound, newsound)
        else:
            newsound = None
        with open(filename, 'w') as f:
            if newsound:
                f.write(f"{newsound}\n next \n")
            else:
                f.write(f"none\n next \n")
            f.write(f"{fps}\n next \n")
            for item in ascii_frames:
                f.write(f"{item}\n next \n")
            f.close()
        input("press enter to view video!")
        if newsound:
            playsound(newsound, block=False)
    else:
        if newsound:
            playsound(sound, block=False)
    timestart = time.time()
    for i, v in enumerate(ascii_frames):
        print(v, flush=True)
        currenttime = time.time() - timestart
        frametime = i / fps
        diff = currenttime - frametime
        if (1.000 / fps) <= diff:
            time.sleep((1.000/fps)/1.8)
        else:
            time.sleep(1.000 / fps + diff)
        # if fps >= 60:
        #     time.sleep(1.000 / fps - ((1.00 / fps) / 4.6))
        # elif fps >= 23 and fps <= 30:
        #     time.sleep(1.000 / fps - ((1.00 / fps) / 4.28))
        # else:
        #     time.sleep(1.000 / fps - ((1.00 / fps) / 5.2))
    if savevid != "y":
        os.remove(sound)

def frames_to_ascii(frame, ratio):
    img = Image.open(frame)
    if ratio <= .59:
        new_width = 220
    elif ratio <= 1:
        new_width = 180
    else:
        new_width = 100
    new_height = ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')
    pixels = img.getdata()
    new_pixels = [ascii_chars[pixel // 25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    ascii_image = ("\n"*int(75*(1-ratio))) + ascii_image
    ascii_frames.append(ascii_image)

def file_to_ascii(file):
    sound = ""
    fps = 1
    with open(file, 'r') as f:
        data = f.read()
        ascii_frames = data.split("next")
        sound = ascii_frames.pop(0)
        sound = sound.strip()
        print(sound)
        fps = ascii_frames.pop(0)
        fps = fps.replace("\n", "").strip()
        fps = float(fps)
    should_check = False
    while should_check == False:
        should_loop = input("loop video? (y for yes, n for no)")
        if should_loop == "y" or should_loop == "n":
            should_check = True
        else:
            print("that is not a valid input!")
    input("press enter to view video!")

    if should_loop == "y":
        while True:
            if sound != "none":
                playsound(sound, block=False)
            timestart = time.time()
            for i, v in enumerate(ascii_frames):
                print(v, flush=True)
                currenttime = time.time() - timestart
                frametime = i / fps
                diff = currenttime - frametime
                if (1.000 / fps) <= diff:
                    time.sleep((1.000 / fps) / 1.8)
                else:
                    time.sleep(1.000 / fps + diff)
    else:
        if sound != "none":
            playsound(sound, block=False)
        timestart = time.time()
        for i, v in enumerate(ascii_frames):
            print(v, flush=True)
            currenttime = time.time() - timestart
            frametime = i / fps
            diff = currenttime - frametime
            if (1.000 / fps) <= diff:
                time.sleep((1.000 / fps) / 1.8)
            else:
                time.sleep(1.000 / fps + diff)

        # if fps >= 60:
        #     time.sleep(1.000/fps - ((1.00/fps)/4.6))
        # elif fps >= 23 and fps <= 30:
        #     time.sleep(1.000 / fps - ((1.00 / fps) / 4.28))
        # else:
        #     time.sleep(1.000 / fps - ((1.00 / fps) / 5.2))

if __name__ == "__main__":
    while True:
        what_to_do = input("would you like to render a new video, or play an existing one? ('r' for render and 'p' for play)\n")
        if what_to_do == "r":
            what_video = input("please paste a valid path to your video, or drag the video here:\n")
            if what_video == "exit": continue
            if " " in what_video:
                print("sorry your video file cannot have spaces in it!")
                continue
            video_to_frames(what_video)
        elif what_to_do == "p":
            what_video = input("please input the name of the .txt file with your video:\n")
            if what_video == "exit": continue
            file_to_ascii(what_video)
        else:
            print("sorry that is not a valid input!")
        ascii_frames = []