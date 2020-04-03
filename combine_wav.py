#coding:utf-8
import os
import wave
import contextlib
import subprocess
#from config import *
import sys

class CombineWav(object):
    '''
    将某个文件夹下面的wav合并
    '''
    def __init__(self):
        pass

    def voice_time(self, path):
        '''
        获取语音文件的时长
        '''
        with contextlib.closing(wave.open(path,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
        duration = frames / float(rate)
        return duration

    def generate_wav(self, wav_files):
        '''
        将多个wav文件合并成多个少于60s的
        '''
        wav_piece=[]
        tmp = []
        total_time = 0
        for file in wav_files:
            time_duration = self.voice_time(file)
            total_time += time_duration
            if total_time > 3000:
                wav_piece.append(tmp)
                total_time = time_duration
                tmp = [file]
            else:
                tmp.append(file)
        wav_piece.append(tmp)
        return wav_piece

    def generate_cmd(self, files, i, target_folder):
        '''
        生成cmd
        '''
        file_text = ' '.join(files)
        text = 'sox --combine concatenate %s %s/%d.wav' % (file_text, target_folder, i)
        return text

    def combine(self, original_folder, target_folder):
        '''
        合并多个wav文件为一个
        '''
        wav_files = os.listdir(original_folder)
        wav_files = sorted(wav_files,key=lambda x:int(x.replace('.wav','').replace('chunk-','')))
        wav_files = [original_folder+'/'+path for path in wav_files]
        wav_piece = self.generate_wav(wav_files)        
        for i, piece in enumerate(wav_piece):
            cmd = self.generate_cmd(piece, i, target_folder)
            subprocess.call(cmd,shell=True)

combine_wav = CombineWav()
if __name__=='__main__':
    original_folder='/data/huangjiaheng/pad_mp3/ipad_asr_corpus'
    target_folder='/data/huangjiaheng/pad_mp3/ipad_asr'
    #original_folder = sys.argv[1]
    #target_folder = sys.argv[2]
    #if not os.path.exists(target_folder):
    #    os.mkdir(target_folder)
    wav_piece = combine_wav.combine(original_folder,target_folder)
