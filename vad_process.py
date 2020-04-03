#coding:utf-8

from __future__ import division
import os
import subprocess
import collections
import contextlib
import sys
import wave
import pkg_resources
import _webrtcvad
import sys

class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

class Vad(object):
    def __init__(self, mode=None):
        self._vad = _webrtcvad.create()
        _webrtcvad.init(self._vad)
        if mode is not None:
            self.set_mode(mode)

    def set_mode(self, mode):
        _webrtcvad.set_mode(self._vad, mode)

    def is_speech(self, buf, sample_rate, length=None):
        #print(buf)
        length = length or int(len(buf) / 2)
        if length * 2 > len(buf):
            raise IndexError(
                'buffer has %s frames, but length argument was %s' % (
                    int(len(buf) / 2.0), length))
        return _webrtcvad.process(self._vad, sample_rate, buf, length)

def valid_rate_and_frame_length(rate, frame_length):
    return _webrtcvad.valid_rate_and_frame_length(rate, frame_length)

class VadProcess(object):
    '''
    将语音文件做VAD
    '''
    def read_wave(self, path):
        with contextlib.closing(wave.open(path, 'rb')) as wf:
            num_channels = wf.getnchannels()
            assert num_channels == 1
            sample_width = wf.getsampwidth()
            assert sample_width == 2
            sample_rate = wf.getframerate()
            assert sample_rate in (8000, 16000, 32000, 48000)
            pcm_data = wf.readframes(wf.getnframes())
            return pcm_data, sample_rate

    def write_wave(self, path, audio, sample_rate):
        with contextlib.closing(wave.open(path, 'wb')) as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio)

    def frame_generator(self, frame_duration_ms, audio, sample_rate):
        '''
        迭代一帧
        '''
        n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
        offset = 0
        timestamp = 0.0
        duration = (float(n) / sample_rate) / 2.0
        while offset + n < len(audio):
            yield Frame(audio[offset:offset + n], timestamp, duration)
            timestamp += duration
            offset += n

    def vad_collector(self, sample_rate, frame_duration_ms, padding_duration_ms, vad, frames):
        num_padding_frames = int(padding_duration_ms / frame_duration_ms)
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False

        voiced_frames = []
        for frame in frames:
            is_speech = vad.is_speech(frame.bytes, sample_rate)

            sys.stdout.write('1' if is_speech else '0')
            if not triggered:
                ring_buffer.append((frame, is_speech))
                num_voiced = len([f for f, speech in ring_buffer if speech])
                if num_voiced > 0.9 * ring_buffer.maxlen:
                    triggered = True
                    sys.stdout.write('+(%s)' % (ring_buffer[0][0].timestamp,))
                    for f, s in ring_buffer:
                        voiced_frames.append(f)
                    ring_buffer.clear()
            else:
                voiced_frames.append(frame)
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                if num_unvoiced > 0.9 * ring_buffer.maxlen:
                    sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
                    triggered = False
                    yield b''.join([f.bytes for f in voiced_frames])
                    ring_buffer.clear()
                    voiced_frames = []
        if triggered:
            sys.stdout.write('-(%s)' % (frame.timestamp + frame.duration))
        sys.stdout.write('\n')
        if voiced_frames:
            yield b''.join([f.bytes for f in voiced_frames])

    def process(self, path, mode,save_path):
        '''
        将wav文件切分成小的vad
        '''
        audio, sample_rate = self.read_wave(path)
        vad = Vad(mode)
        frames = self.frame_generator(30, audio, sample_rate)
        frames = list(frames)
        segments = self.vad_collector(sample_rate, 20, 300, vad, frames)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        for i, segment in enumerate(segments):
            path = '%s/chunk-%002d.wav' % (save_path, i)
            print(' Writing %s' % (path,))
            self.write_wave(path, segment, sample_rate)

process_vad=VadProcess()
if __name__ == '__main__':
    #待VAD的wav文件路径
    path = sys.argv[1]
    #path = '/data/sale_crm_wavs/003D5FDC58B795C201D3677E3F6D253DF682270400B50C977F4F14D99EB63E8D_left.wav'
    #VAD之后的wav文件保存的文件夹
    save_path = sys.argv[2]
    #save_path = '/data/save'
    mode=3
    process_vad.process(path, mode, save_path)
