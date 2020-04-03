#coding:utf-8
import os
import wave

def wav_time(pathdir):
    times = 0
    for rootdir, filedir , filenames in os.walk(pathdir):
        for filename in filenames:
            path = os.path.join(rootdir, filename)
            xfile = wave.open(path)
            time = xfile.getparams()[3] / xfile.getparams()[2]
            times +=time
    return times

























