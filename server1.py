#coding:utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

import re, sys
import json
import os
import numpy as np
from scipy.io import wavfile
import subprocess
import hmac
import base64
import hashlib
import time
import requests

from video_handle import download_video
from vad_process import process_vad
from config import *
from denoise import de_noise
from combine_wav import wav_combine

define ('port', default=8000, help='run on the given port', type= int)

class YituTranslate(object):
    '''
    调用依图接口
    '''
    def __init__(self):
        self.ASR_URL = 'http://asr-prod.yitutech.com/v2/asr'
        self.AUDIO_AUE = 'pcm'
        self.DevId = '2194'
        self.DevKey = 'bdda7535f6f74a1d81736eeb190140fe'
        self.lang = 1  
        self.scene = 0
        self.aue = ''

    def translate(self, AUDIO_PATH):
        '''
        将语音转换成文本
        '''
        time_ts = str(int(time.time()))
        param_string = str(self.DevId) + time_ts
        sign = hmac.new(self.DevKey.encode(), param_string.encode(), digestmod=hashlib.sha256).hexdigest()
        headers = {'x-dev-id': str(self.DevId), 'x-request-send-timestamp': time_ts, 'x-signature': sign}

        # 消息实体
        useCustomWordsIds = [] # 用户自定义热词库ID
        with open(AUDIO_PATH, "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read())
            basee64_file = encoded_string.decode('utf-8')
        body = {'audioBase64': basee64_file, 'lang': self.lang, 'scene': self.scene, 'aue': self.AUDIO_AUE,
                'useCustomWordsIds': useCustomWordsIds}

        # 发起请求
        r = requests.post(self.ASR_URL, json=body, headers=headers)
        if r.status_code != 200:
            return r.status_code, r.json()
        return r.json()['rtn'], r.json()['resultText']

yitu_translate=YituTranslate()
class Product():
    def parse_wav(self,folder): 
        files=os.listdir(folder)
        files = sorted(files,key=lambda x:int(x.replace('.wav','')))
        print(files)
        files = [os.path.join(folder,file) for file in files]
        total_text = []
        for file in files:
            code,text = yitu_translate.translate(file)
            if text:
                print(text)
                total_text.append(text)
        return total_text
    
    def get(self, url, by_time = False):
        #download video
        download_video.retrieve(url, VIDEO_MP4_PATH)
        #vad
        de_noise.produce(VOICE_PATH, VOICE_PATH_CLEAN)
        mode = 0
        process_vad.process(VOICE_PATH_CLEAN, mode, VAD_PATH)
        #字典
        total_text = self.parse_wav(VAD_PATH)
        wav_combine.combine(VAD_PATH,COMBINE_PATH)
        
        #获取时长和去除完静音之后的比值
        video_time = combine_wav.voice_time()
        rm_mute_time = combine_wav.voice_time()
        if video_time != 0:
            ratio = rm_mute_time/video_time
        else:
            ratio = 1

        with open(AUDIO_PATH, "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read())
            basee64_file = encoded_string.decode('utf-8')
        body = {'audioBase64': basee64_file,'video_time':video_time,
                'rm_mute':rm_mute_time,'ratio':ratio}
        temp = json.dumps(body)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(temp)

#curl http://localhost:8000/start/https://cs-dianhua-record-backup-1251661065.cos.ap-beijing.myqcloud.com/20191024/10-3-1-57/B412C045DE0AA52E21DD84651E650917B3E766216A2454AFE9D419F9204DA9128DD24D4AEE8AFE5A.wav
if __name__ == "__main__":
    product = Product()
    url = 'https:\/\/ym-zm-nvr-cos-1251661065.cos.ap-beijing.myqcloud.com\/BeijingWangfujin\/ch47_2019-11-8-19:50:34-2019-11-8-20:0:9'
    product.get(url)
