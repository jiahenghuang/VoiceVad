# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function 
import numpy as np
import wave  
import math
from ctypes import *
import sys

class DeNoise(object):
    '''
    给wav文件降噪
    '''
    def __init__(self):
        pass

    def produce(self, filename, savename):
        '''
        降噪
        '''
        ll = cdll.LoadLibrary   
        lib = ll("./build/lib.linux-x86_64-2.7/_simple_ns.so")  

        chunk = 160 
        dataout = np.zeros((160))  
        dataout = dataout.astype(np.int16)

        f = wave.open(filename,"rb") 
        pms = f.getparams()
        nchannels, sampwidth, framerate, nframes = pms[:4]

        cycle = int(math.ceil(nframes/chunk))
        dataoutall = np.zeros(cycle*160)  
        dataoutall = dataoutall.astype(np.int16)

        lib.webrtc_nsx_create.restype=c_void_p
        a = lib.webrtc_nsx_create(2)

        for j in range(cycle):
            data = f.readframes(chunk)  
            data = np.fromstring(data, np.int16)

            b_arr = (c_short*160)(*dataout)
            a_arr = (c_short*160)(*data)

            lib.webrtc_nsx_process(a, a_arr, b_arr)
            
            for i in range(160):
                dataoutall[i + j*160] = b_arr[i]

        dataoutall = dataoutall.tostring()
        wave_out=wave.open(savename,'w')
        wave_out.setnchannels(1)
        wave_out.setsampwidth(2)
        wave_out.setframerate(8000)
        wave_out.writeframes(dataoutall)

de_noise = DeNoise()
if __name__=='__main__':
    #待降噪的wav文件路径
    filename = ''
    #降噪后保存的wav文件路径
    savename = ''
    de_noise.produce(filename, savename)

