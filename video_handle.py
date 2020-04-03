#coding:utf-8
from urllib import request
import subprocess

class VideoDownload(object):
    '''
    下载视频
    '''
    def __init__(self):
        pass

    def retrieve(self, url, mp4_path):
        '''
        抽取视频中音频
        '''
        url = url.replace('\','')
        request.urlretrieve(url, mp4_path)
        wav_path = mp4_path.replace('.mp4', '.wav')
        cmd = 'ffmpeg -i %s %s' % (mp4_path, wav_path)
		subprocess.call(cmd,shell=True)

download_video=VideoDownload()
if __name__=='__main__':
    url = 'https:\/\/ym-zm-nvr-cos-1251661065.cos.ap-beijing.myqcloud.com\/BeiJingGuomao1\/ch16_2019-11-1-19:14:58-2019-11-1-19:20:34'
    mp4_path = ''
    download_video.retrieve(url, mp4_path)
