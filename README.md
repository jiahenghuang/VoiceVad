本项目实现降噪和VAD功能。
1. 降噪 
   python3 denoise.py 
2. VAD
   python3 vad_process.py
3. 拼接音频
   将1.wav,2.wav,3.wav拼接成combine.wav
   sox --combine concatenate 1.wav 2.wav 3.wav combine.wav

关于VAD中的mode设置：
取值范围为：0,1,2,3
值越大，文件切的越碎

正常流程：
1. 降噪
2. 对降噪后的文件进行VAD


备注：
暂时只看降噪和VAD功能就好了，其他的代码文件暂时用不到。