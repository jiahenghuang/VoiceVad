import requests


# curl --request POST    --url https://open.workec.com/auth/accesstoken    --header 'cache-control: no-cache'    --header 'content-type: application/json'  --data '{	"appId": appId,	"appSecret": "appSecret"}'

headers = {
    'cache-control': 'no-cache',
    'content-type': 'application/json'}

data = '{\t"/https:\/\/ym-zm-nvr-cos-1251661065.cos.ap-beijing.myqcloud.com\/BeiJingGuomao1\/ch16_2019-11-1-19:14:58-2019-11-1-19:20:34"}'
response = requests.post('http://localhost:8000/start/', headers=headers, data=data)
http://localhost:8000/start
def ToFile(txt, file):
    with open(txt, 'r') as fileObj:
        base64_data = fileObj.read()
        ori_image_data = base64.b64decode(base64_data)
        fout = open(file, 'wb')
        fout.write(ori_image_data)
        fout.close()