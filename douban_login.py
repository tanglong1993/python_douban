import requests
import re
from PIL import Image
import base64

login_url = 'https://accounts.douban.com/login'
check_url = 'https://www.douban.com/people/174625786/'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}

login_data = {
    'source':'index_nav',
    'redir':'https://www.douban.com/',
    'form_email':'*****',   #输入注册邮箱
    'form_password':'****',  #输入密码
    'captcha-solution':'',
    'captcha-id':'',
    'login':'登录'
}

#获取验证码图片并返回验证码ID
def get_captcha(content):
    pattern = re.compile(r'<img id="captcha_image" src="(.*?)"',re.S)
    pattern_id = re.compile(r'<input type="hidden" name="captcha-id" value="(.*?)"/>',re.S)
    captcha_imgs = re.findall(pattern,content)
    captcha_id = re.findall(pattern_id,content)
    if len(captcha_imgs)> 0:
        try:
            r = requests.get(captcha_imgs[0])
            with open('captcha.png','wb') as f:
                f.write(r.content)
            im = Image.open('captcha.png')
            im.show()
        except Exception as e:
            print('打开图片出错')
    if len(captcha_id)> 0:
        return captcha_id[0]
    else:
        print('没有找到ID')
        return None

##使用识别验证码api，识别图片，但是我使用的这个api，识别不准确
# def identify_captcha():
#     appkey = '26a753c0c748c7f14d79d136c21519d6'
#     sub_url = 'http://op.juhe.cn/vercode/index'
#     code_type = '1005'
#     image_path = 'captcha.png'
#     params = {
#         'key':appkey,
#         'codeType':code_type,
#         'image':'',
#         'base64Str':'',
#         'dtype':''
#     }
#     with open(image_path,'rb') as f:
#         params['base64Str'] = base64.b64encode(f.read())
#     print(params)
#     r = requests.post(url=sub_url,data=params)
#     print(r.status_code)
#     print(r.text)
#     captcha_code = re.findall(r'"result":"(.*?)"',r.text)
#     print(captcha_code)
#     return captcha_code[0]

session = requests.session()
r = session.get(url=login_url)
login_data['captcha-id'] = get_captcha(r.text)
login_data['captcha-solution'] = input("请输入验证码的值：")
print(login_data)
r = session.post(url=login_url,headers=headers,data=login_data)
print(r.text)






