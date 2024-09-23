import os
import requests
import re
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')

data = {
    'email': email,
    'passwd': password,
}

headers = {
    'authority': 'dounai.pro',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://dounai.pro/user',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.37',
}

# 获取COOKIE值
cookie_jar = requests.Session().post('https://dounai.pro/auth/login', headers=headers, data=data).cookies
cookies = requests.utils.dict_from_cookiejar(cookie_jar)



panel = requests.get('https://dounai.pro/user/panel', cookies=cookies, headers=headers)
checkin = requests.post('https://dounai.pro/user/checkin', cookies=cookies,headers=headers)



meg = '签到：' + checkin.text.encode().decode("unicode_escape")


email_password = os.environ.get('ADDRESS_PASSWORD')
from_address = os.environ.get('FROM_ADDRESS')
receiver_address = os.environ.get('RECEIVER_ADDRESS')

# 邮件基本信息
smtp_server = "smtp.qq.com"
smtp_port = 465

# 邮件构造
message = MIMEText(meg, "plain", "utf-8")
message["From"] = Header(from_address)
message["To"] = Header(receiver_address, "utf-8")
message["Subject"] = Header("来自豆豆豆奶的签到信息", "utf-8")

# 发送邮件
smtpObject = smtplib.SMTP_SSL(smtp_server, smtp_port)
smtpObject.login(from_address, email_password)
smtpObject.sendmail(from_address, [receiver_address], message.as_string())
smtpObject.quit()
