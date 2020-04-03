#coding:utf-8
import shutil
import os
import subprocess

folder_path = '/data/ai/important-data/pad_mp3/more_result'
files = os.listdir(folder_path)
save_path = '/data/ai/important-data/pad_mp3/more_result_vad'
files = [line for line in files if 'left' in line]
for i,file in enumerate(files):
		print(i/len(files))
		path = os.path.join(folder_path, file)
		file_name = file.replace('.wav','')
		folder_name = save_path+'/'+file_name
		if not os.path.exists(folder_name):
			os.mkdir(folder_name)
			cmd = 'python2 vad_process.py %s %s'%(path, folder_name)
			subprocess.call(cmd, shell=True)
	
