#coding:utf-8
import shutil
import os
import subprocess

folder_path = '/data/huangjiaheng/pad_mp3/more_result_vad'
folders = os.listdir(folder_path)

for folder in folders:
	try:
		x_folder = os.path.join(folder_path, folder)
		if not os.path.exists('/data/huangjiaheng/pad_mp3/ipad_corpus/%s' % folder):
			os.mkdir('/data/huangjiaheng/pad_mp3/ipad_corpus/%s' % folder)
			cmd = 'python3 combine_wav.py %s /data/huangjiaheng/pad_mp3/ipad_corpus/%s'%(x_folder, folder)
			subprocess.call(cmd, shell=True)
		if not os.listdir('/data/huangjiaheng/pad_mp3/ipad_corpus/%s' % folder):
			shutil.rmtree('/data/huangjiaheng/pad_mp3/ipad_corpus/%s' % folder)
	except:
		pass
