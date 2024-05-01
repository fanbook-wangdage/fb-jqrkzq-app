"""
分离的机器人控制器安卓版api文件
"""

from flask import Flask, request, render_template,redirect,abort
import requests
import sentry_sdk

sentry_sdk.init(
    dsn="https://d4dda36b62424e467aed986688d469fa@o4506171336753152.ingest.sentry.io/4506591217254400",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
) 

import ctypes
import json
import time
import random
import threading
from pygments import highlight#高亮
from pygments.lexers import JsonLexer#高亮
from pygments.formatters import TerminalFormatter#高亮
from colorama import Fore, Back, Style,init#高亮
from flask_cors import CORS
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def colorize_json(smg2,pcolor=''):
    json_data=smg2
    try:
        parsed_json = json.loads(json_data)  # 解析JSON数据
        formatted_json = json.dumps(parsed_json, indent=4)  # 格式化JSON数据

        # 使用Pygments库进行语法高亮
        colored_json = highlight(formatted_json, JsonLexer(), TerminalFormatter())

        print(colored_json)
    except json.JSONDecodeError as e:
        print(json_data)

def addmsg(msg, color="white"):
    if color == "white":
        print(msg)
    elif color == "red":
        print("\033[31m" + msg + "\033[39m")
    elif color == "yellow":
        print("\033[33m" + msg + "\033[39m")
    elif color == "green":
        print("\033[32m" + msg + "\033[39m")
    elif color == "aqua":
        print("\033[36m" + msg + "\033[39m")
init(autoreset=True)
def colorprint(smg2,pcolor):
    if pcolor=='red':
      print(Fore.RED + smg2)
    elif pcolor=='bandg':
      print(Back.GREEN + smg2)
    elif pcolor=='d':
      print(Style.DIM + smg2)
 
# 获取控制台窗口句柄
kernel32 = ctypes.windll.kernel32
hwnd = kernel32.GetConsoleWindow()

# 设置窗口标题
if hwnd != 0:
    kernel32.SetConsoleTitleW("api终端进程-1")
 
ip_list=[]
ipsl_list=[]

def fzjc(client_ip):
    global ip_list,ipsl_list
    if client_ip not in ip_list:
        ip_list.append(client_ip)
        ipsl_list.append(1)
        return False
    else:
        if ipsl_list[ip_list.index(client_ip)]>=100:
            print(f'请求过多，ip:{client_ip}')
            return True
        else:
            ipsl_list[ip_list.index(client_ip)]+=1
            return False

ucode=[]
users=[]

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    return render_template('i.html',userip=client_ip)


@app.errorhandler(500)
def internal_server_error(e):
    time.sleep(2)
    return render_template('errors.html'), 500


@app.route('/api/sentry', methods=['POST'])
def sentry():
    json_data = request.json
    print(json_data)
    colorize_json(smg2=json_data)
    return {'ok':True}


@app.route('/dl1/')
def dl1():
    #return '失败，api已弃用，请更新到最新版本'
    global ucode
    global users
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    code1=request.args.get('code')
    if code1 in ucode: 
        cd1=users[ucode.index(code1)]
        ind=ucode.index(code1)
        users.pop(ind)
        ucode.pop(ind)
        return cd1
    else:
        return 'none'

users_data=[]
tokens=[]

@app.route('/app/login', methods=['GET'])
def applogin():
    global ucode
    global users,users_data,tokens
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    code1=request.args.get('code')
    if code1 in ucode: 
        cd1=users[ucode.index(code1)]
        ind=ucode.index(code1)
        users.pop(ind)
        ucode.pop(ind)
        return f'ok-{tokens[ucode.index(code1)]}-成功'
    else:
        return 'err-0-登录失败，请检查验证码'

@app.route('/web/gettoken', methods=['GET'])
def gettoken():
    global users_data,tokens,ucode,users
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    code = request.args.get('code')
    Type = request.args.get('type')
    try:
        # 定义请求参数
        token_url = "https://a1.fanbook.mobi/open/oauth2/token"
        redirect_uri = "http://1.117.76.68:5000/dl"
        # 构建请求头
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic NTYyMTIyMjIwOTE5NDU5ODQwOndhWHdDb216RWZkcVQwdnhqbEdyZUNWb2FERUttY3Zx"
        }
        # 构建请求体参数
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }
        # 发送POST请求获取访问令牌
        response = requests.post(token_url, headers=headers, data=data)
        lp=response.text
        print(response.text)
        # 解析响应
        if response.status_code == 200:
            token_data = response.json()
            url="https://a1.fanbook.mobi/open/api/user/getMe"
            headers = {
                "content-type": "application/json",
                "authorization": "Basic "+token_data["access_token"]
            }
            response = requests.post(url, headers=headers)
            print(response.text)
            user_data = response.json()
            ucode.append('')
            users.append('')
            users_data.append({"ok":"true","username":user_data["data"]["nickname"],"userid":user_data["data"]["user_id"],"avatar":user_data["data"]["avatar"]})
            tokens.append(generate_random_string(15))
            return {"ok":"true","token":tokens[-1]}
        if Type != "az":
            return {"ok":"false","token":""}
        else:
            return f'ok-{tokens[-1]}'
    except:
        if Type != "az":
            return {"ok":"false","token":""}
        else:
            return 'err-0'
    
@app.route('/web/tokeninfo', methods=['GET'])
def tokeninfo():
    client_ip = request.remote_addr
    Type = request.args.get('type')
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    global users_data,tokens
    token = request.args.get('token')
    try:
        if Type != "az":
            return users_data[tokens.index(token)]
        else:
            return f'ok-{users_data[tokens.index(token)]["username"]}-{users_data[tokens.index(token)]["userid"]}-{users_data[tokens.index(token)]["avatar"]}'
    except:
        if Type != "az":
            return {"ok":"false"}
        else:
            return 'err-0'

@app.route('/dl/')
def dl():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    global ucode
    global users,users_data
    code = request.args.get('code')
    m = request.args.get('state')
    print(code)
    if m=='1':
        #返回重定向和code
        return redirect(f"http://1.117.76.68:8005/index.html?code={code}&fb_redirect&open_type=mp")
    elif m=='gettoken':
        token_url = "https://a1.fanbook.mobi/open/oauth2/token"
        redirect_uri = "http://1.117.76.68:5000/dl"
        # 构建请求头
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic NTYyMTIyMjIwOTE5NDU5ODQwOndhWHdDb216RWZkcVQwdnhqbEdyZUNWb2FERUttY3Zx"
        }
        # 构建请求体参数
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }
        # 发送POST请求获取访问令牌
        response = requests.post(token_url, headers=headers, data=data)
        lp=response.text
        print(response.text)
        token_data = response.json()
        return token_data["access_token"]
    else:
        if True:
            # 定义请求参数
            token_url = "https://a1.fanbook.mobi/open/oauth2/token"
            redirect_uri = "http://1.117.76.68:5000/dl"
            # 构建请求头
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic NTYyMTIyMjIwOTE5NDU5ODQwOndhWHdDb216RWZkcVQwdnhqbEdyZUNWb2FERUttY3Zx"
            }
            # 构建请求体参数
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri
            }
            # 发送POST请求获取访问令牌
            response = requests.post(token_url, headers=headers, data=data)
            lp=response.text
            print(response.text)
            # 解析响应
            if response.status_code == 200:
                token_data = response.json()
                url="https://a1.fanbook.mobi/open/api/user/getMe"
                headers = {
                    "content-type": "application/json",
                    "authorization": "Basic "+token_data["access_token"]
                }
                response = requests.post(url, headers=headers)
                print(response.text)
                user_data = response.json()
                print(user_data)
                cd=random.randint(100000,999999)
                ucode.append(str(cd))
                users.append(str(user_data["data"]["username"]))
                tokens.append(generate_random_string(15))
                users_data.append({"ok":"true","username":user_data["data"]["nickname"],"userid":user_data["data"]["user_id"],"avatar":user_data["data"]["avatar"]})
                return '验证码获取成功，验证码：'+str(cd)

@app.route('/bot/getme',methods=['GET'])
def getme():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    botdata=request.args.get('data')
    url='https://a1.fanbook.mobi/api/bot/'+botdata+'/getMe'
    headers = {'content-type':"application/json;charset=utf-8"}
    jsonfile=json.dumps({})
    postreturn=requests.post(url,data=jsonfile,headers=headers)
    print(postreturn.text)
    apitext=postreturn.text
    return str(apitext)

@app.route('/bot/getme1',methods=['GET'])
def getme1():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    botdata=request.args.get('data')
    url='https://a1.fanbook.mobi/api/bot/'+botdata+'/getMe'
    headers = {'content-type':"application/json;charset=utf-8"}
    jsonfile=json.dumps({})
    postreturn=requests.post(url,data=jsonfile,headers=headers)
    print(postreturn.text)
    try:
        return {"data":json.loads(postreturn.text),"errorInfo":"","status":"OK"}
    except: 
        return {"data":"","errorInfo":"token错误","status":"error"}

@app.route('/bot/getmsg',methods=['GET'])
def getmsg():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    try:
        bottoken=request.args.get('token')
        pdid=request.args.get('pdid')
        retype=request.args.get('type')
        url = f"https://a1.fanbook.mobi/api/bot/{bottoken}/message/getList"
        payload = json.dumps({
        "channel_id": str(pdid),
        "size": "1"
        })
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        msgdata=json.loads(response.text)
        if retype=="1":
            return {"messageid":msgdata["data"][0]["message_id"],"text":json.loads(msgdata["data"][0]["content"])["text"]}
        else:
            return msgdata["data"][0]
    except:
        return "获取失败"

@app.route('/bot/sm',methods=['GET','POST'])
def sm():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    botdata=request.args.get('token')
    pdid=request.args.get('chatid')
    text=request.args.get('text')
    m=request.args.get('m')
    fwqid=request.args.get('fwqid')
    if m=='sx':
        url = f"https://a1.fanbook.mobi/api/bot/{botdata}/searchGuildMemberByName"
        payload = json.dumps({
        "guild_id": int(fwqid),
        "username": [
            str(pdid)
        ]})
        headers = {
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.text)
        pdid=json.loads(response.text)["result"][0]["user"]["id"]
        url=f'https://a1.fanbook.mobi/api/bot/{botdata}/getPrivateChat'#获取私聊频道
        headers={'Content-Type': 'application/json'}
        body=json.dumps({"user_id":int(pdid)})
        r=requests.post(url,headers=headers,data=body)
        pdid=json.loads(r.text)["result"]["id"]
        url='https://a1.fanbook.mobi/api/bot/'+botdata+'/sendMessage'
        headers = {'content-type':"application/json;charset=utf-8"}
        jsonfile=json.dumps({"chat_id":int(pdid),"text":str(text)})
        postreturn=requests.post(url,data=jsonfile,headers=headers)
        print(postreturn.text)
    else:
        url='https://a1.fanbook.mobi/api/bot/'+botdata+'/sendMessage'
        headers = {'content-type':"application/json;charset=utf-8"}
        jsonfile=json.dumps({"chat_id":int(pdid),"text":str(text)})
        postreturn=requests.post(url,data=jsonfile,headers=headers)
        print(postreturn.text)
    try:
        return '成功，消息id:'+str(json.loads(postreturn.text)["result"]["message_id"])
    except: 
        return "无法完成请求，没有权限或者机器人没有发言api白名单"


@app.route('/bot/delmsg',methods=['GET'])
def delmsg():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    botdata=request.args.get('token')
    msgid=request.args.get('msgid')
    chatid=request.args.get('chatid')
    url='https://a1.fanbook.mobi/api/bot/'+botdata+'/deleteMessage'
    headers = {'content-type':"application/json;charset=utf-8"}
    jsonfile=json.dumps({"chat_id":int(chatid),"message_id":int(msgid)})
    postreturn=requests.post(url,data=jsonfile,headers=headers)
    print(postreturn.text)
    try:
        return {"data":"成功撤回此消息","errorInfo":"","status":"OK"}
    except: 
        return {"data":"失败","errorInfo":"无法完成请求，参数错误或者机器人没有权限","status":"error"}


def color16(c=''):
    if len(c)<6 or len(c)>8 or len(c)%2 != 0:
        return True
    else:
        return False

@app.route('/bot/fsmessagekp', methods=['GET', 'POST'])
def fsmessagekp():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    bottoken = request.args.get('token')
    btwz = request.args.get('btwz')
    btys = request.args.get('btys')
    btysb = request.args.get('btysb')
    jbs = request.args.get('jbs')
    wbnr=request.args.get('wbnr')
    qyan = request.args.get('qyan')
    anwb = request.args.get('anwb')
    anlj = request.args.get('anlj')
    pdid=request.args.get('pdid')
    anys=request.args.get('anys')
    btwbys=request.args.get('btwbys')
    #替换wbnr中的'\n'为'  \\\\n'
    wbnr=wbnr.replace('\n',r'  \\\\\n')
    #如果颜色不符合16进制格式：
    if color16(btys) or color16(btysb) or color16(anys) or color16(btwbys):
        return '颜色不符号16进制格式，请确保颜色长度为6-8位，且长度为偶数'
    else:
        if str(jbs)=='t':
            if str(qyan)=='t':
                url = f"https://a1.fanbook.mobi/api/bot/{bottoken}/sendMessage"
                payload = json.dumps({
                "chat_id": int(pdid),
                "text": "{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"gradient\\\":{\\\"colors\\\":[\\\""+str(btys)+"\\\",\\\""+str(btysb)+"\\\"]},\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+str(btwz)+"\\\",\\\"style\\\":{\\\"color\\\":\\\"#"+str(btwbys)+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\"ddeeff\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,0,0,4\\\",\\\"alignment\\\":\\\"-1,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+str(wbnr)+"\\\"}},{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,12,0,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"button\\\",\\\"category\\\":\\\"outlined\\\",\\\"color\\\":\\\"#"+str(anys)+"\\\",\\\"size\\\":\\\"medium\\\",\\\"widthUnlimited\\\":true,\\\"href\\\":\\\""+str(anlj)+"\\\",\\\"label\\\":\\\""+str(anwb)+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}"
                })
                
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
                return '发送成功'
            else:
                url = f"https://a1.fanbook.mobi/api/bot/{bottoken}/sendMessage"
                payload = json.dumps({
                "chat_id": int(pdid),
                "text": "{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"gradient\\\":{\\\"colors\\\":[\\\""+str(btys)+"\\\",\\\""+str(btysb)+"\\\"]},\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+str(btwz)+"\\\",\\\"style\\\":{\\\"color\\\":\\\"#"+str(btwbys)+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\"ddeeff\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,0,0,4\\\",\\\"alignment\\\":\\\"-1,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+str(wbnr)+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}"
                })
                
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
                return '发送成功'
        else:
            if str(qyan)=='t':
                url = f"https://a1.fanbook.mobi/api/bot/{bottoken}/sendMessage"
                payload = json.dumps({
                "chat_id": int(pdid),
                "text": "{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"gradient\\\":{\\\"colors\\\":[\\\""+str(btys)+"\\\",\\\""+str(btys)+"\\\"]},\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+str(btwz)+"\\\",\\\"style\\\":{\\\"color\\\":\\\"#"+str(btwbys)+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\"ddeeff\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,0,0,4\\\",\\\"alignment\\\":\\\"-1,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+str(wbnr)+"\\\"}},{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,12,0,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"button\\\",\\\"category\\\":\\\"outlined\\\",\\\"color\\\":\\\"#"+str(anys)+"\\\",\\\"size\\\":\\\"medium\\\",\\\"widthUnlimited\\\":true,\\\"href\\\":\\\""+str(anlj)+"\\\",\\\"label\\\":\\\""+str(anwb)+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}"
                })
                
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
                return '发送成功'
            else:
                url = f"https://a1.fanbook.mobi/api/bot/{bottoken}/sendMessage"
                payload = json.dumps({
                "chat_id": int(pdid),
                "text": "{\"width\":null,\"height\":null,\"data\":\"{\\\"tag\\\":\\\"column\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"12,7\\\",\\\"gradient\\\":{\\\"colors\\\":[\\\""+str(btys)+"\\\",\\\""+str(btys)+"\\\"]},\\\"child\\\":{\\\"tag\\\":\\\"text\\\",\\\"data\\\":\\\""+str(btwz)+"\\\",\\\"style\\\":{\\\"color\\\":\\\"#"+str(btwbys)+"\\\",\\\"fontSize\\\":16,\\\"fontWeight\\\":\\\"medium\\\"}},\\\"backgroundColor\\\":\\\"ddeeff\\\"},{\\\"tag\\\":\\\"container\\\",\\\"child\\\":{\\\"tag\\\":\\\"column\\\",\\\"padding\\\":\\\"12\\\",\\\"children\\\":[{\\\"tag\\\":\\\"container\\\",\\\"padding\\\":\\\"0,0,0,4\\\",\\\"alignment\\\":\\\"-1,0\\\",\\\"child\\\":{\\\"tag\\\":\\\"markdown\\\",\\\"data\\\":\\\""+str(wbnr)+"\\\"}}]},\\\"backgroundColor\\\":\\\"ffffff\\\"}],\\\"crossAxisAlignment\\\":\\\"stretch\\\"}\",\"notification\":null,\"come_from_icon\":null,\"come_from_name\":null,\"template\":null,\"no_seat_toast\":null,\"type\":\"messageCard\"}"
                })
                
                headers = {
                'Content-Type': 'application/json'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)
                return '发送成功'

@app.route('/app/getnew', methods=['GET'])
def getnew():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    return '5 1.8更新：修复界面bug http://1.117.76.68/app/kzq18.apk'



rungptuser=[]
xcbz=[]
xcm=[]
true=True

@app.route('/rungpt/')
def rungpt():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    global rungptuser
    global xcbz
    global xcm
    userdid=request.args.get('user')
    token=request.args.get('token')
    botid=request.args.get('botid')
    apikey=request.args.get('apikey')
    pdid=request.args.get('pdid')
    if userdid not in rungptuser:
        rungptuser.append(str(userdid))
        xcbz.append(True)
        xcm.append('gptybs'+str(userdid))
    if xcbz[rungptuser.index(userdid)] == False:
        return '你已经达到最大限制，请先停止一个进程再启动'
    else:
        url='https://a1.fanbook.mobi/api/bot/'+str(token)+'/sendMessage'
        headers = {'content-type':"application/json;charset=utf-8"}
        jsonfile=json.dumps({
        "chat_id":int(pdid),
        "text":"[ChatGPT云部署]\n权限验证消息\n[王大哥机器人控制器]"
        })
        print(jsonfile)
        postreturn=requests.post(url,data=jsonfile,headers=headers)
        csfh=json.loads(postreturn.text)
        if csfh['ok'] == true:
            xcbz[rungptuser.index(userdid)]=False
            t1 = threading.Thread(target=thread1,args=(token,botid,apikey,rungptuser.index(userdid)),name='gptybs'+str(userdid))
            t1.start()
            return '成功，你的进程编号：'+'gptybs'+str(userdid)
        else:
            return '失败，你的机器人没有发言api白名单或者没有权限'

@app.route('/getjc/')
def getjc():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    global rungptuser,xcm
    userdid=request.args.get('user')
    if userdid in rungptuser:
        return xcm[rungptuser.index(userdid)]
    else:
        return '无进程'

@app.route('/scjc/')
def scjc():
    client_ip = request.remote_addr
    if fzjc(client_ip=client_ip):
        abort(429, '429-Too Many Requests [请求过快，休息一下嘛~ ヾ(≧▽≦*)o]')
    global rungptuser,xcm,xcbz
    userdid=request.args.get('user')
    if userdid in rungptuser:
        xcbz[rungptuser.index(userdid)]=True
        return '成功，进程会在1分钟内结束'
    else:
        return '你没有需要结束的进程'

def thread1(lingpai='',bot_id='',api_key='',runbz=0):
    global ms
    global xz
    global sycyid,cysycs,jgczsj,dycs,hhxxlb,hhidlb,messages,qgglb,xcbz,rungptuser
    global gjc,fwqlb,fwqxz,fwqms,efzdy,mxlb,hhpdidlb,xxjl,xxfsz,xxfszid,xcm
    import requests#http请求
    import json#json数据处理
    import traceback#错误捕获
    import urllib.request
    import time#延时
    import websocket#ws接口链接
    import base64#请求体编码
    import threading
    import queue
    import random
    from pygments import highlight#高亮
    from pygments.lexers import JsonLexer#高亮
    from pygments.formatters import TerminalFormatter#高亮
    from colorama import init, Fore, Back, Style#高亮
    import urllib.request
    import ssl
    import sentry_sdk
    import threading
    import openai

    #openai.api_base = "https://api.chatanywhere.com.cn/v1"
    openai.api_base = "https://openkey.cloud/v1"

    messages = []
    openai.api_key=api_key

    sentry_sdk.init(
        dsn="https://a30ed1f97ae54e663e8cf7db6928b17d@o4506171336753152.ingest.sentry.io/4506176633896960",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0,
    )
    init(autoreset=True)  #初始化自动恢复颜色，多次执行会导致卡慢
    b=0
    for s in range(1):
        try:
            zdsxw=6
            b+=1
            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
            headers = {'content-type':"application/json;charset=utf-8"}
            jsonfile=json.dumps({
            "chat_id":54509346087282944,
            "text":"ChatGPT服务启动[beta 4.6]\n标识号:FREE1\n第"+str(s+1)+"次，共30次"
            })
            print(jsonfile)
            postreturn=requests.post(url,data=jsonfile,headers=headers)
            def get_audio_duration(url,msg):
                """
                try:
                    # 要下载的文件的URL
                    file_url = url

                    # 从URL中提取文件名
                    file_name = os.path.basename(file_url)

                    # 构建文件的保存路径
                    save_path = os.path.join(os.getcwd(), file_name)
                    filename=file_name
                    # 下载文件并保存到程序根目录
                    urllib.request.urlretrieve(url, filename)
                    print(f"文件已下载到：{filename}")
                except Exception as e:
                    print(f"下载出错：{e}")
                # 获取音频文件的时长
                filepath = filename
                """
                # 获取到的时长单位为秒
                return len(msg) // 4
            '''
            url = "https://speech.ai.xiaomi.com/speech/1.0/tts_token?token=eyJ2IjoiVjAiLCJuIjoiU1oifQ.AAAXUkp9P1QAFgBdFAwbZ24VTkoaRRsPG2AFFhgAQgBIRyIvRw4PfR9GGBh0VUBPEQhHWxBrPkBITxBDEFhHb1RHT0FXEw0QY20QRU4AWgBZTTJVQQ4YTE9KEXF2AAkUSRNMGBh0XUdeQRtQQ31hahBOGRJPQwlGMwUXHBFdQV5ANmhBTk0UTkEPFW4BQXMUWUECR2A-QEtIEkJHXBM3VRtKFQsSAxpgYxceGBVFEBRPJgMAAAAKR0xLMD99FB8ATABeR2NVQBlHWw8KEjE7D0kaERcPAkBlBA8YR1tEDkBqbxQcQhNUDhhLN0QAFhNYGwkTY2IVSkMOVEdCUnQKExobXRACE2ZtGgA.EO5fMqpLGoC6LrZI3pQP5w"
            audio_duration = get_audio_duration(url)
            print(f"音频时长：{audio_duration} 秒")
            '''
            ms='0'
            sycyid=[]#使用成员id
            cysycs=[]#成员使用次数
            jgczsj=0#警告重置时间
            gjc=''#绘图关键词
            dycs=0#本次总调用次数
            fwqlb=[]#服务器列表
            fwqxz=[]#服务器选择角色
            fwqms=[]#服务器选择的模式
            efzdy=0#二分钟调用次数
            zdyzyxx=False#是否只打印重要信息，可能会影响性能
            mxlb=[]#模型列表
            hhxxlb=[]#绘画消息列表
            hhpdidlb=[]#频道id列表
            hhidlb=[]#绘画id列表
            xxjl=[]#消息记录
            xxfszid=[]#消息发送者列表
            xxfsz=[]#消息发送者用户名
            qgglb=[]#去广告服务器id列表
            dljclb=[]#独立进程服务器id列表
            
            def get_ad(adjl=10,fwqid=0):
                global qgglb
                fsad=random.randint(1,adjl)
                gg=''
                gglb=[""]
                if adjl==1 or adjl==2 or adjl==3:
                    gg=gglb[random.randint(0,len(gglb)-1)]
                    print(gg)
                if str(fwqid) in qgglb:
                    return ''
                else:
                    return gg
            def bot_send_message(token=lingpai,pdid=0,text=''):
                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                headers = {'content-type':"application/json;charset=utf-8"}
                jsonfile=json.dumps({
                "chat_id":pdid,
                "text":text
                })
                print(jsonfile)
                postreturn=requests.post(url,data=jsonfile,headers=headers)
                colorize_json(smg2=postreturn.text,pcolor='d')
            allrw='空, 荧, 派蒙, 纳西妲, 阿贝多, 温迪, 枫原万叶, 钟离, 荒泷一斗, 八重神子, 艾尔海森, 提纳里, 迪希雅, 卡维, 宵宫, 莱依拉, 赛诺, 诺艾尔, 托马, 凝光, 莫娜, 北斗, 神里绫华, 雷电将军, 芭芭拉, 鹿野院平藏, 五郎, 迪奥娜, 凯亚, 安柏, 班尼特, 琴, 柯莱, 夜兰, 妮露, 辛焱, 珐露珊, 魈, 香菱, 达达利亚, 砂糖, 早柚, 云堇, 刻晴, 丽莎, 迪卢克, 烟绯, 重云, 珊瑚宫心海, 胡桃, 可莉, 流浪者, 久岐忍, 神里绫人, 甘雨, 戴因斯雷布, 优菈, 菲谢尔, 行秋, 白术, 九条裟罗, 雷泽, 申鹤, 迪娜泽黛, 凯瑟琳, 多莉, 坎蒂丝, 萍姥姥, 罗莎莉亚, 留云借风真君, 绮良良, 瑶瑶, 七七, 奥兹, 米卡, 夏洛蒂, 埃洛伊, 博士, 女士, 大慈树王, 三月七, 娜塔莎, 希露瓦, 虎克, 克拉拉, 丹恒, 希儿, 布洛妮娅, 瓦尔特, 杰帕德, 佩拉, 姬子, 艾丝妲, 白露, 星, 穹, 桑博, 伦纳德, 停云, 罗刹, 卡芙卡, 彦卿, 史瓦罗, 螺丝咕姆, 阿兰, 银狼, 素裳, 丹枢, 黑塔, 景元, 帕姆, 可可利亚, 半夏, 符玄, 公输师傅, 奥列格, 青雀, 大毫, 青镞, 费斯曼, 绿芙蓉, 镜流, 信使, 丽塔, 失落迷迭, 缭乱星棘, 伊甸, 伏特加女孩, 狂热蓝调, 莉莉娅, 萝莎莉娅, 八重樱, 八重霞, 卡莲, 第六夜想曲, 卡萝尔, 姬子, 极地战刃, 布洛妮娅, 次生银翼, 理之律者, 真理之律者, 迷城骇兔, 希儿, 魇夜星渊, 黑希儿, 帕朵菲莉丝, 天元骑英, 幽兰黛尔, 德丽莎, 月下初拥, 朔夜观星, 暮光骑士, 明日香, 李素裳, 格蕾修, 梅比乌斯, 渡鸦, 人之律者, 爱莉希雅, 爱衣, 天穹游侠, 琪亚娜, 空之律者, 终焉之律者, 薪炎之律者, 云墨丹心, 符华, 识之律者, 维尔薇, 始源之律者, 芽衣, 雷之律者, 苏莎娜, 阿波尼亚, 陆景和, 莫弈, 夏彦, 左然'
            allrw=allrw.split(', ')
            print(allrw)
            xz=''
            false=False
            data_queue = queue.Queue()
            def on_message(ws, message):
                try:
                    global ms
                    global xz
                    global sycyid,cysycs,jgczsj,dycs,hhxxlb,hhidlb,messages
                    global gjc,fwqlb,fwqxz,fwqms,efzdy,mxlb,hhpdidlb,xxjl,xxfsz,xxfszid
                    # 处理接收到的消息
                    if zdyzyxx == False:
                        addmsg('收到消息',color='green')
                        colorize_json(message)
                    message=json.loads(message)
                    if message["action"] =="push":
                        if message["data"]["author"]["bot"] == false:
                            if str(message["data"]["guild_id"]) in dljclb:
                                pass
                            else: 
                                content = json.loads(message["data"]["content"])
                                userid=message["data"]["user_id"]
                                fwqid=message["data"]["guild_id"]
                                if "${@!"+str(bot_id)+"}" in content['text']:
                                    if zdyzyxx:
                                        addmsg('收到重要消息',color='green')
                                        colorize_json(message)
                                    efzdy+=1
                                    dycs+=1
                                    if fwqid in fwqlb:
                                        print('服务器id:',fwqid,'已经记录过，不需要重新记录')
                                    else:
                                        fwqlb.append(fwqid)
                                        fwqms.append("0")
                                        fwqxz.append('')
                                        mxlb.append('ChatGPT')
                                        messages.append([])
                                        print('服务器id:',fwqid,'已经成功被记录')
                                        print(fwqlb)
                                    if userid in sycyid:
                                        sycy=sycyid.index(userid)
                                        cysycs[sycy]+=1
                                        print('用户id:',userid,'使用次数增加1,原本次数为：',cysycs[sycy])
                                    else:
                                        sycyid.append(userid)
                                        cysycs.append(1)
                                        print('新使用用户：',userid)
                                        print(sycyid)
                                        print(cysycs)
                                    if int(cysycs[sycyid.index(userid)]) == 7:
                                        print('用户：',userid,'第6次操作')
                                        url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                        headers = {'content-type':"application/json;charset=utf-8"}
                                        jsonfile=json.dumps({
                                        "chat_id":int(message["data"]["channel_id"]),
                                        "text": '速率限制：\n你当前给机器人发送消息数超过每两分钟6次，请休息一下，2分钟后再来吧'+get_ad(adjl=2,fwqid=fwqid),
                                        "reply_to_message_id":int(message["data"]["message_id"])
                                        })
                                        print(jsonfile)
                                        postreturn=requests.post(url,data=jsonfile,headers=headers)
                                        colorize_json(smg2=postreturn.text,pcolor='d')
                                    elif int(cysycs[sycyid.index(userid)]) < 7:
                                        if '模式切换' in content['text']:
                                            if mxlb[fwqlb.index(fwqid)] == 'ChatGPT':
                                                if fwqms[fwqlb.index(fwqid)]=='0':
                                                    fwqms[fwqlb.index(fwqid)]='1'
                                                    fwqxz[fwqlb.index(fwqid)]=''
                                                    url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                    headers = {'content-type':"application/json;charset=utf-8"}
                                                    jsonfile=json.dumps({
                                                    "chat_id":int(message["data"]["channel_id"]),
                                                    "text": '回复模式已切换为语音回复模式(默认为派蒙[喵娘属性])\n可通过快捷指令[切换人物]切换'+get_ad(adjl=2,fwqid=fwqid),
                                                    "reply_to_message_id":int(message["data"]["message_id"])
                                                    })
                                                    print(jsonfile)
                                                    postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                    colorize_json(smg2=postreturn.text,pcolor='d')
                                                else:
                                                    fwqms[fwqlb.index(fwqid)]='0'
                                                    url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                    headers = {'content-type':"application/json;charset=utf-8"}
                                                    jsonfile=json.dumps({
                                                    "chat_id":int(message["data"]["channel_id"]),
                                                    "text": '回复模式已切换为文本模式',
                                                    "reply_to_message_id":int(message["data"]["message_id"])
                                                    })
                                                    print(jsonfile)
                                                    postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                    colorize_json(smg2=postreturn.text,pcolor='d')
                                            else:
                                                fwqms[fwqlb.index(fwqid)]='0'
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text": '抱歉，暂时只有ChatGPT支持模式切换，其他均为文本输出，请切换模型为ChatGPT再切换模式'+get_ad(adjl=2,fwqid=fwqid),
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif '可选人物' in content['text']:
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text": "${@!"+message["data"]["user_id"]+"}"+'所有可选人物列表：空, 荧, 派蒙, 纳西妲, 阿贝多, 温迪, 枫原万叶, 钟离, 荒泷一斗, 八重神子, 艾尔海森, 提纳里, 迪希雅, 卡维, 宵宫, 莱依拉, 赛诺, 诺艾尔, 托马, 凝光, 莫娜, 北斗, 神里绫华, 雷电将军, 芭芭拉, 鹿野院平藏, 五郎, 迪奥娜, 凯亚, 安柏, 班尼特, 琴, 柯莱, 夜兰, 妮露, 辛焱, 珐露珊, 魈, 香菱, 达达利亚, 砂糖, 早柚, 云堇, 刻晴, 丽莎, 迪卢克, 烟绯, 重云, 珊瑚宫心海, 胡桃, 可莉, 流浪者, 久岐忍, 神里绫人, 甘雨, 戴因斯雷布, 优菈, 菲谢尔, 行秋, 白术, 九条裟罗, 雷泽, 申鹤, 迪娜泽黛, 凯瑟琳, 多莉, 坎蒂丝, 萍姥姥, 罗莎莉亚, 留云借风真君, 绮良良, 瑶瑶, 七七, 奥兹, 米卡, 夏洛蒂, 埃洛伊, 博士, 女士, 大慈树王, 三月七, 娜塔莎, 希露瓦, 虎克, 克拉拉, 丹恒, 希儿, 布洛妮娅, 瓦尔特, 杰帕德, 佩拉, 姬子, 艾丝妲, 白露, 星, 穹, 桑博, 伦纳德, 停云, 罗刹, 卡芙卡, 彦卿, 史瓦罗, 螺丝咕姆, 阿兰, 银狼, 素裳, 丹枢, 黑塔, 景元, 帕姆, 可可利亚, 半夏, 符玄, 公输师傅, 奥列格, 青雀, 大毫, 青镞, 费斯曼, 绿芙蓉, 镜流, 信使, 丽塔, 失落迷迭, 缭乱星棘, 伊甸, 伏特加女孩, 狂热蓝调, 莉莉娅, 萝莎莉娅, 八重樱, 八重霞, 卡莲, 第六夜想曲, 卡萝尔, 姬子, 极地战刃, 布洛妮娅, 次生银翼, 理之律者, 真理之律者, 迷城骇兔, 希儿, 魇夜星渊, 黑希儿, 帕朵菲莉丝, 天元骑英, 幽兰黛尔, 德丽莎, 月下初拥, 朔夜观星, 暮光骑士, 明日香, 李素裳, 格蕾修, 梅比乌斯, 渡鸦, 人之律者, 爱莉希雅, 爱衣, 天穹游侠, 琪亚娜, 空之律者, 终焉之律者, 薪炎之律者, 云墨丹心, 符华, 识之律者, 维尔薇, 始源之律者, 芽衣, 雷之律者, 苏莎娜, 阿波尼亚, 陆景和, 莫弈, 夏彦, 左然\n请使用切换人物指令切换，仅在语音回复模式生效'+get_ad(adjl=2,fwqid=fwqid),
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif '切换人物' in content['text']:
                                            fwqxz[fwqlb.index(fwqid)]=content['text'][31:-1]
                                            print(fwqxz[fwqlb.index(fwqid)])
                                            if str(fwqxz[fwqlb.index(fwqid)]) in allrw:
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text": '人物已切换为:'+fwqxz[fwqlb.index(fwqid)],
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                            else:
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text": '找不到你选择的人物：'+fwqxz[fwqlb.index(fwqid)]+'\n请确认你输入的人物在可选人物列表中'+get_ad(adjl=2,fwqid=fwqid),
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif '运行节点信息' in content['text']:
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text": "${@!"+message["data"]["user_id"]+"}"+'当前运行节点信息：\n运行节点名：王大哥ChatGPT部署工具1.0\n近期累计调用次数：'+str(dycs)+'次\n2分钟内调用次数：'+str(efzdy)+'次\n版本号：4.3\n新功能体验/反馈，欢迎前往：https://fanbook.mobi/LmgLJF3N'+get_ad(adjl=2,fwqid=fwqid),
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif 'AI绘图' in content['text']:
                                            gjc=content['text'][31:-1]
                                            print('关键词:',gjc)
                                            htmessage=requests.get('https://api.lolimi.cn/api/ai/mj1?key=sWlckPY0hlgaDryj7hnLewOjTU&msg='+str(gjc), stream=True)
                                            print(htmessage.text)
                                            htmessage=json.loads(htmessage.text)
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text":"请稍等....\n正在努力生成图片，你的图片id为："+str(htmessage['data'])+"\n请在一分钟后再来查看此消息，或者使用命令：[获取绘图图片]来获取生成的图片\n你的关键词/表达式为："+gjc+get_ad(adjl=2,fwqid=fwqid),
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                            hhdata = json.loads(postreturn.text)
                                            hhxxlb.append(hhdata["result"]["message_id"])
                                            hhidlb.append(str(htmessage['data']))
                                            hhpdidlb.append(str(message["data"]["channel_id"]))
                                        elif '获取绘图图片' in content['text']:
                                            gjc=content['text'][33:-1]
                                            print('图片id:',gjc)
                                            htmessage=requests.get('https://api.lolimi.cn/api/ai/mj2?key=sWlckPY0hlgaDryj7hnLewOjTU&id='+str(gjc), stream=True)
                                            print(htmessage.text)
                                            htmessage=json.loads(htmessage.text)
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text":"{\"type\":\"richText\",\"title\":\"图片获取成功\",\"document\":\"[{\\\"insert\\\":\\\"111111111\\\\n测试\\\\n\\\\n[图片]\\\\n\\\"}]\",\"v2\":\"[{\\\"insert\\\":\\\"进度："+str(htmessage['data'])+"\\\\n\\\\n\\\\n\\\"},{\\\"insert\\\":{\\\"name\\\":\\\"paste_image_1693622751346.png\\\",\\\"source\\\":\\\""+str(htmessage["imageurl"])+"\\\",\\\"width\\\":1800.0,\\\"height\\\":2912.0,\\\"checkPath\\\":null,\\\"_type\\\":\\\"image\\\",\\\"_inline\\\":false}},{\\\"insert\\\":\\\"\\\\n\\\\n\\\"}]\",\"v\":2}",
                                            "parse_mode": "Fanbook",
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif '切换模型' in content['text']:
                                            if 'ChatGPT' in content['text']:
                                                mxlb[fwqlb.index(fwqid)] = 'ChatGPT'
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text":"模型已切换为ChatGPT"+get_ad(adjl=2,fwqid=fwqid),
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                            elif '文心一言' in content['text']:
                                                mxlb[fwqlb.index(fwqid)] = '文心一言'
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text":"模型已切换为文心一言"+get_ad(adjl=2,fwqid=fwqid),
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                            elif '星火大模型V2.0' in content['text']:
                                                mxlb[fwqlb.index(fwqid)] = '星火大模型V2.0'
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text":"模型已切换为星火大模型V2.0"+get_ad(adjl=2,fwqid=fwqid),
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                            else:
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text":"找不到你选择的模型，请重新选择"+get_ad(adjl=2,fwqid=fwqid),
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif 'system_message' in content['text']:
                                            print(content['text'][37:])
                                            system_message=content['text'][37:]
                                            messages[fwqlb.index(fwqid)].append({"role":"system","content":system_message})
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text":'系统消息添加成功:'+content['text'][37:]+'\n当前上下文列表:\n'+str(messages[fwqlb.index(fwqid)])+'\n最大上下文长度:'+str(zdsxw),
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif '清除上下文' in content['text']:
                                            messages[fwqlb.index(fwqid)]=[]
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text":"${@!"+message["data"]["user_id"]+"}"+'清除上下文成功\n最大上下文长度:'+str(zdsxw)+get_ad(adjl=2,fwqid=fwqid),
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                        elif 'system_run_py' in content['text']:
                                            print(content['text'][36:])
                                            code=content['text'][36:]
                                            pdid=int(message["data"]["channel_id"])
                                            try:
                                                exec(code, globals())
                                            except Exception as e:
                                                error=traceback.format_exc()
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text":'执行失败，原因：\n'+error+'\ncode:\n'+code,
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                            headers = {'content-type':"application/json;charset=utf-8"}
                                            jsonfile=json.dumps({
                                            "chat_id":int(message["data"]["channel_id"]),
                                            "text":'执行完毕',
                                            "reply_to_message_id":int(message["data"]["message_id"])
                                            })
                                            print(jsonfile)
                                            postreturn=requests.post(url,data=jsonfile,headers=headers)
                                            colorize_json(smg2=postreturn.text,pcolor='d')
                                            
                                        else:
                                            if fwqms[fwqlb.index(fwqid)]=='0':
                                                #text=json.loads(content)
                                                print(mxlb[fwqlb.index(fwqid)]+'文本模式回复')
                                                print(content['text'])
                                                print(content['text'][23:])
                                                print(messages[fwqlb.index(fwqid)])
                                                if mxlb[fwqlb.index(fwqid)] == 'ChatGPT':
                                                    if len(messages[fwqlb.index(fwqid)]) > zdsxw:
                                                        sc=messages[fwqlb.index(fwqid)][0]
                                                        sc2=messages[fwqlb.index(fwqid)][1]
                                                        messages[fwqlb.index(fwqid)].pop(0)
                                                        messages[fwqlb.index(fwqid)].pop(1)
                                                        print('删除了上下文'+str(sc)+str(sc2)+'\n剩余长度'+str(len(messages[fwqlb.index(fwqid)])))
                                                    a=''
                                                    #chatmessage=requests.get('https://api.lolimi.cn/API/AI/mfcat3.5.php?type=json&format=0&sx= &msg='+content['text'][23:]+'.', stream=True)
                                                    messages[fwqlb.index(fwqid)].append({"role":"user","content": content['text'][23:]})
                                                    zt=0
                                                    for resp in openai.ChatCompletion.create(
                                                                                        model="gpt-3.5-turbo",
                                                                                        messages=messages[fwqlb.index(fwqid)],
                                                                                        # 流式输出
                                                                                        stream = True):
                                                        if 'content' in resp.choices[0].delta:
                                                            if zt==0:
                                                                zt=1
                                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                                jsonfile=json.dumps({
                                                                "chat_id":int(message["data"]["channel_id"]),
                                                                "text": resp.choices[0].delta.content,
                                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                                })
                                                                print(jsonfile)
                                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                                                messageinfo=postreturn.text
                                                                messageinfo=json.loads(messageinfo)
                                                            a+=resp.choices[0].delta.content
                                                            print(resp.choices[0].delta.content, end="", flush=True)
                                                            print(a)
                                                            if random.randint(0,100)<25:
                                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/editMessageText'
                                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                                jsonfile=json.dumps({
                                                                "chat_id":int(message["data"]["channel_id"]),
                                                                "message_id":messageinfo['result']['message_id'],
                                                                "text": a,
                                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                                })
                                                                print(jsonfile)
                                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                                    url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/editMessageText'
                                                    headers = {'content-type':"application/json;charset=utf-8"}
                                                    jsonfile=json.dumps({
                                                    "chat_id":int(message["data"]["channel_id"]),
                                                    "message_id":messageinfo['result']['message_id'],
                                                    "text": a,
                                                    "reply_to_message_id":int(message["data"]["message_id"])
                                                    })
                                                    print(jsonfile)
                                                    postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                    colorize_json(smg2=postreturn.text,pcolor='d')
                                                    reply = a
                                                    print(reply)
                                                    chatmessage=reply
                                                    messages[fwqlb.index(fwqid)].append({"role": "assistant", "content": chatmessage})
                                                elif mxlb[fwqlb.index(fwqid)] == '文心一言':
                                                    chatmessage=requests.get('https://api.lolimi.cn/API/AI/wx.php?type=json&format=0&msg='+content['text'][23:], stream=True)
                                                    chatmessage=json.loads(chatmessage.text)
                                                elif mxlb[fwqlb.index(fwqid)] == '星火大模型V2.0':
                                                    chatmessage=requests.get('https://api.lolimi.cn/API/AI/xh.php?type=json&format=0&msg='+content['text'][23:]+'.', stream=True)
                                                    chatmessage=json.loads(chatmessage.text)
                                                print(chatmessage)
                                                n="""
            """
                                                if mxlb[fwqlb.index(fwqid)] == '星火大模型V2.0' or mxlb[fwqlb.index(fwqid)] == '文心一言':
                                                    url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                    headers = {'content-type':"application/json;charset=utf-8"}
                                                    jsonfile=json.dumps({
                                                    "chat_id":int(message["data"]["channel_id"]),
                                                    "text": chatmessage['data']['output'].replace('\n', n)+get_ad(adjl=8,fwqid=fwqid),
                                                    "reply_to_message_id":int(message["data"]["message_id"]),
                                                    })
                                                    print(jsonfile)
                                                    postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                    colorize_json(smg2=postreturn.text,pcolor='d')
                                                '''
                                                else:
                                                    #chatmessage=chatmessage['data'].replace('\\\\', '\\')
                                                    chatmessage=chatmessage.replace('\\n', n)
                                                    text=chatmessage.replace('', '')+get_ad(adjl=8)
                                                    url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                    headers = {'content-type':"application/json;charset=utf-8"}
                                                    jsonfile=json.dumps({
                                                    "chat_id":int(message["data"]["channel_id"]),
                                                    "text": "${@!"+message["data"]["user_id"]+"}"+text+get_ad(adjl=8,fwqid=fwqid),
                                                    #"parse_mode":"Fanbook",
                                                    "reply_to_message_id":int(message["data"]["message_id"])
                                                    })
                                                    print(jsonfile)
                                                    postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                    colorize_json(smg2=postreturn.text,pcolor='d')
                                                '''
                                            elif fwqms[fwqlb.index(fwqid)]=='1':
                                                print('音频模式回复')
                                                print(content['text'])
                                                print(content['text'][23:])
                                                if fwqxz[fwqlb.index(fwqid)] == '':
                                                    chatmessage=requests.get('https://api.lolimi.cn/API/AI/ys3.5.php?msg=.'+content['text'][23:], stream=True)
                                                else:
                                                    chatmessage=requests.get('https://api.lolimi.cn/API/AI/ys3.5.php?msg=.'+content['text'][23:]+'&speaker='+xz, stream=True)
                                                chatmessage=json.loads(chatmessage.text)
                                                print(chatmessage)
                                                print(chatmessage['music'])
                                                url = chatmessage['music']
                                                audio_duration = get_audio_duration(str(url),msg=chatmessage['msg'])
                                                print(f"音频时长：{audio_duration} 秒")
                                                xx='{"type": "voice","url": "'+chatmessage['music']+'","second": '+str(int(audio_duration))+',"isRead": false}'
                                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                                                headers = {'content-type':"application/json;charset=utf-8"}
                                                jsonfile=json.dumps({
                                                "chat_id":int(message["data"]["channel_id"]),
                                                "text": xx,
                                                "reply_to_message_id":int(message["data"]["message_id"])
                                                })
                                                print(jsonfile)
                                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                                colorize_json(smg2=postreturn.text,pcolor='d')
                                            xxjl.append(mxlb[fwqlb.index(fwqid)]+'模式回复消息:'+content['text'][23:].replace('\n', '')+'，模型回复:'+str(chatmessage).replace('\n', ''))
                                            xxfsz.append('发送者:'+message["data"]["author"]["nickname"]+message["data"]["author"]["username"])
                                            xxfszid.append('userid:'+message['data']["user_id"]+" 服务器id:"+str(fwqid))
                                    else:
                                        print('用户：',userid,'已经操作过快，忽略输入')
                except Exception as e:
                    if 'KeyError' in traceback.format_exc():
                        pass
                    else:
                        error=traceback.format_exc()
                        print(error)
                        url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                        headers = {'content-type':"application/json;charset=utf-8"}
                        jsonfile=json.dumps({
                        "chat_id":54509346038728244,
                        "text":"发生错误:\n"+error
                        })
                        print(jsonfile)
                        postreturn=requests.post(url,data=jsonfile,headers=headers)
                        colorize_json(smg2=postreturn.text,pcolor='d')
                # 在这里添加你希望执行的操作
            def on_error(ws, error):
                # 处理错误
                if 'KeyError' in traceback.format_exc():
                    pass
                else:
                    error=traceback.format_exc()
                    addmsg("发生错误:"+str(error),color='red')
                    print(error)
                    url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                    headers = {'content-type':"application/json;charset=utf-8"}
                    jsonfile=json.dumps({
                    "chat_id":54509346038782944,
                    "text":"发生错误:\n"+error
                    })
                    print(jsonfile)
                    postreturn=requests.post(url,data=jsonfile,headers=headers)
                    colorize_json(smg2=postreturn.text,pcolor='d')
            def on_close(ws):
                # 连接关闭时的操作
                addmsg("连接已关闭",color='red')
                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                headers = {'content-type':"application/json;charset=utf-8"}
                jsonfile=json.dumps({
                "chat_id":54509346038782944,
                "text":"ws连接被关闭"
                })
                print(jsonfile)
                postreturn=requests.post(url,data=jsonfile,headers=headers)
                colorize_json(smg2=postreturn.text,pcolor='d')
            def on_open(ws):
                # 连接建立时的操作
                addmsg("连接已建立",color='green')
                # 发送心跳包
                def send_ping():
                    print('发送：{"type":"ping"}')
                    ws.send('{"type":"ping"}')
                send_ping()  # 发送第一个心跳包
                # 定时发送心跳包
                def schedule_ping():
                    send_ping()
                    """
                    # 每25秒发送一次心跳包
                    websocket._get_connection()._connect_time = 0  # 重置连接时间，避免过期
                    ws.send_ping()
                    websocket._get_connection().sock.settimeout(70)
                    ws.send('{"type":"ping"}')
                    """
                #websocket._get_connection().run_forever(ping_interval=25, ping_payload='{"type":"ping"}', ping_schedule=schedule_ping)
            # 替换成用户输入的BOT令牌
            lingpai = lingpai
            url = f"https://a1.fanbook.mobi/api/bot/{lingpai}/getMe"
            # 发送HTTP请求获取基本信息
            response = requests.get(url)
            data = response.json()
            def send_data_thread():
                global sycyid,cysycs,jgczsj,efzdy,hhxxlb,hhidlb,hhpdidlb,xxfsz,xxjl,xxfszid,xcbz,rungptuser,xcm
                while True:
                    if xcbz[runbz]:
                        break
                    """
                    for x in range(3):
                        cpu_res = psutil.cpu_percent(interval=1)
                        
                    print(cpu_res/3)
                    """
                    # 在这里编写需要发送的数据
                    time.sleep(17)
                    ws.send('{"type":"ping"}')
                    addmsg('发送心跳包：{"type":"ping"}',color='green')
                    if len(xxjl) != len(xxfsz) or len(xxjl) != len(xxfszid) or len(xxjl) != len(xxfszid):
                        url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
                        headers = {'content-type':"application/json;charset=utf-8"}
                        jsonfile=json.dumps({
                        "chat_id":54509346032944,
                        "text":"[dev 1]\n[警告]\n[BUG]消息记录数据异常，已尝试清除"
                        })
                        print(jsonfile)
                        postreturn=requests.post(url,data=jsonfile,headers=headers)
                        xxjl=[]
                        xxfsz=[]
                        xxfszid=[]
                    jgczsj+=1
                    for i in hhidlb:
                        z=hhpdidlb[hhidlb.index(i)]
                        sy=hhidlb.index(i)
                        try:
                            htmessage=requests.get('https://api.lolimi.cn/api/ai/mj2?key=sWlckPY0hlgaDryj7hnLewOjTU&id='+str(i), stream=True)
                            print(htmessage.text)
                            htmessage=json.loads(htmessage.text)
                            if str(htmessage['data']) != "100%":
                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/editMessageText'
                                headers = {'content-type':"application/json;charset=utf-8"}
                                jsonfile=json.dumps({
                                "chat_id":int(z),
                                "text": "{\"type\":\"richText\",\"title\":\"图片正在生成，请稍等...\",\"document\":\"[{\\\"insert\\\":\\\"111111111\\\\n测试\\\\n\\\\n[图片]\\\\n\\\"}]\",\"v2\":\"[{\\\"insert\\\":\\\"进度："+str(htmessage['data'])+"\\\\n\\\\n\\\\n\\\"},{\\\"insert\\\":{\\\"name\\\":\\\"paste_image_1693622751346.png\\\",\\\"source\\\":\\\""+str(htmessage["imageurl"])+"\\\",\\\"width\\\":1800.0,\\\"height\\\":2912.0,\\\"checkPath\\\":null,\\\"_type\\\":\\\"image\\\",\\\"_inline\\\":false}},{\\\"insert\\\":\\\"\\\\n\\\\n\\\"}]\",\"v\":2}",
                                "message_id":int(hhxxlb[hhidlb.index(i)]),
                                "parse_mode": "Fanbook"
                                })
                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                colorize_json(smg2=postreturn.text,pcolor='d')
                            else:
                                url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/editMessageText'
                                headers = {'content-type':"application/json;charset=utf-8"}
                                jsonfile=json.dumps({
                                "chat_id":int(z),
                                "text": "{\"type\":\"richText\",\"title\":\"图片生成完成\",\"document\":\"[{\\\"insert\\\":\\\"111111111\\\\n测试\\\\n\\\\n[图片]\\\\n\\\"}]\",\"v2\":\"[{\\\"insert\\\":\\\"进度："+str(htmessage['data'])+"\\\\n\\\\n\\\\n\\\"},{\\\"insert\\\":{\\\"name\\\":\\\"paste_image_1693622751346.png\\\",\\\"source\\\":\\\""+str(htmessage["imageurl"])+"\\\",\\\"width\\\":1800.0,\\\"height\\\":2912.0,\\\"checkPath\\\":null,\\\"_type\\\":\\\"image\\\",\\\"_inline\\\":false}},{\\\"insert\\\":\\\"\\\\n\\\\n\\\"}]\",\"v\":2}",
                                "message_id":int(hhxxlb[hhidlb.index(i)]),
                                "parse_mode": "Fanbook"
                                })
                                print(jsonfile)
                                postreturn=requests.post(url,data=jsonfile,headers=headers)
                                colorize_json(smg2=postreturn.text,pcolor='d')
                                hhidlb.pop(sy)
                                hhpdidlb.pop(sy)
                                hhxxlb.pop(sy)
                        except Exception as e:
                            try:
                                if str(htmessage["pointout"]) == "请耐心等待出图":
                                    pass
                                else:
                                    hhidlb.pop(sy)
                                    hhpdidlb.pop(sy)
                                    hhxxlb.pop(sy)
                            #hhidlb.pop(sy)
                            #hhpdidlb.pop(sy)
                            #hhxxlb.pop(sy)
                            except Exception as e:
                                pass
                            pass
                    print('当前警告重置时间：',str(jgczsj))
                    if jgczsj >= 10:
                        print('警告重置')
                        jgczsj=0
                        efzdy=0
                        sycyid=[]#使用成员id
                        cysycs=[]#成员使用次数
                        #hhpdidlb.clear()
                        #hhidlb.clear()
                        #hhxxlb.clear()
            if response.ok and data.get("ok"):
                user_token = data["result"]["user_token"]
                device_id = "your_device_id"
                version_number = "1.6.60"
                super_str = base64.b64encode(json.dumps({
                    "platform": "bot",
                    "version": version_number,
                    "channel": "office",
                    "device_id": device_id,
                    "build_number": "1"
                }).encode('utf-8')).decode('utf-8')
                ws_url = f"wss://gateway-bot.fanbook.mobi/websocket?id={user_token}&dId={device_id}&v={version_number}&x-super-properties={super_str}"
                threading.Thread(target=send_data_thread, daemon=True).start()
                # 建立WebSocket连接
                websocket.enableTrace(True)
                ws = websocket.WebSocketApp(ws_url,
                                            on_message=on_message,
                                            on_error=on_error,
                                            on_close=on_close)
                ws.on_open = on_open
                ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            else:
                addmsg("无法获取BOT基本信息，请检查令牌是否正确。",color='red')
            '''
            xx='{"type": "voice","url": "https://speech.ai.xiaomi.com/speech/1.0/tts_token?token=eyJ2IjoiVjAiLCJuIjoiU1oifQ.AAAXUkp9P1QAFgBdFAwbZ24VTkoaRRsPG2AFFhgAQgBIRyIvRw4PfR9GGBh0VUBPEQhHWxBrPkBITxBDEFhHb1RHT0FXEw0QY20QRU4AWgBZTTJVQQ4YTE9KEXF2AAkUSRNMGBh0XUdeQRtQQ31hahBOGRJPQwlGMwUXHBFdQV5ANmhBTk0UTkEPFW4BQXMUWUECR2A-QEtIEkJHXBM3VRtKFQsSAxpgYxceGBVFEBRPJgMAAAAKR0xLMD99FB8ATABeR2NVQBlHWw8KEjE7D0kaERcPAkBlBA8YR1tEDkBqbxQcQhNUDhhLN0QAFhNYGwkTY2IVSkMOVEdCUnQKExobXRACE2ZtGgA.EO5fMqpLGoC6LrZI3pQP5w","second": '+str(int(audio_duration))+',"isRead": false}'

            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
            headers = {'content-type':"application/json;charset=utf-8"}
            jsonfile=json.dumps({
            "chat_id":int(pdid),
            "text": xx
            })
            postreturn=requests.post(url,data=jsonfile,headers=headers)
            colorize_json(smg2=postreturn.text,pcolor='d')
            '{\"type\":\"richText\",\"title\":\"\",\"document\":\"[{\\\"insert\\\":\\\"111111111\\\\n测试\\\\n\\\\n[图片]\\\\n\\\"}]\",\"v2\":\"[{\\\"insert\\\":\\\"111111111\\\\n测试\\\\n\\\\n\\\"},{\\\"insert\\\":{\\\"name\\\":\\\"paste_image_1693622751346.png\\\",\\\"source\\\":\\\"https://fb-cdn.fanbook.mobi/fanbook/app/files/chatroom/unKnow/df8ce32b1e5e6990d4d958343a4b973d.png\\\",\\\"checkPath\\\":null,\\\"_type\\\":\\\"image\\\",\\\"_inline\\\":false}},{\\\"insert\\\":\\\"\\\\n\\\\n\\\"}]\",\"v\":2}","entities":[]}}'
            '''
        except Exception as e:
            print(str(traceback.format_exc()))
            #global b
            url='https://a1.fanbook.mobi/api/bot/'+lingpai+'/sendMessage'
            headers = {'content-type':"application/json;charset=utf-8"}
            jsonfile=json.dumps({
            "chat_id":54509346038282944,
            "text":"发生异常:\n"+str(traceback.format_exc())+"\n尝试次数:"+str(b)+"/30\n尝试重新启动..."
            })
            print(jsonfile)
            postreturn=requests.post(url,data=jsonfile,headers=headers)
            print(postreturn.text)
            continue

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
