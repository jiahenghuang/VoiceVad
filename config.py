#coding:utf-8
import os

VIDEO_PATH='/root/video_download/tmp.mp4'
WAV_PATH='/root/video_download/tmp.wav'
VAD_PATH='/root/vad_folder/'

if not os.path.exists(VIDEO_PATH):
    os.mkdir(VIDEO_PATH)

if not os.path.exists(WAV_PATH):
    os.mkdir(WAV_PATH)

if not os.path.exists(VAD_PATH):
    os.mkdir(VAD_PATH)