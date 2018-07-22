'''自动监控Linux服务器并发送警报消息到邮箱和微信中'''
# 需要安装 psutil 和 wechatpy ，还有 pycrypto 或者 cryptography
# pip install pycrypto  cryptography  2选1
# pip3 install psutil wechatpy
import psutil, time

class monitor:
    # get the hostname
    host = psutil.users()[0].name

    cpu_data = []

    @classmethod
    def mem(cls, max=65):
        used = psutil.virtual_memory().percent
        if used > max:
            cls.mail("你的主机-'{}'内存空间已使用{}%，超过{}%，请注意!".format(cls.host, used, max))
            cls.wechat("你的主机-'{}'内存空间已使用{}%，超过{}%，请注意!".format(cls.host, used, max))
            print("你的主机-'{}'内存空间已使用{}%，超过{}%，请注意!".format(cls.host, used, max))

    @classmethod
    def cpu(cls, max=20):
        used = psutil.cpu_percent(1)   #interval is 1 second
        cls.cpu_data.append(used)
        if len(cls.cpu_data) >= 3:
            avg = sum(cls.cpu_data) / len(cls.cpu_data)
            if used > max:
                cls.mail("你的主机-[{}]cpu负载已达到{}%，超过{}%，请注意！".format(cls.host, used, max))
                cls.wechat("你的主机-[{}]cpu负载已达到{}%，超过{}%，请注意！".format(cls.host, used, max))
                print("你的主机-[{}]cpu负载已达到{}%，超过{}%，请注意！".format(cls.host, used, max))
            cls.cpu_data.pop()

    @classmethod
    def mail(cls, content):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        nickname = "Automatic Monitor Program"

        # sender info
        sender = "847497935@qq.com"
        password = "<qq邮箱授权码>"         #邮箱密码或授权码        

        # getter info
        receiver = "1347638091@qq.com"

        # message
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = formataddr([nickname, sender])
        msg['Subject'] = 'Automatic alarm!'

        server = smtplib.SMTP_SSL('smtp.qq.com', 465)

        try:
            # login and send the message
            server.login(sender, password)
            server.sendmail(sender, [receiver], msg.as_string())
        except Exception as err:
            print(err)
        finally:
            server.quit()

    @classmethod
    def wechat(cls, content):
        '''wechat send template message'''
        from wechatpy import WeChatClient
        import datetime

        client = WeChatClient('<appID>', '<appsecret>')   # appID and appsecret
        template_id = '<模板ID>'                       # 模板ID
        openid = '<关注该公众号之后的用户列表ID>'    # 关注该公众号之后的用户列表ID

        data = {
            'msg': {'value': content, 'color': '#173177'},
            'time': {'value': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'color': '#173177'},
        }

        try:
            client.message.send_template(openid, template_id, data)
        except Exception as err:
            print(err)

    @classmethod
    def send_msg(cls):
        cls.mem()
        cls.cpu()

while True:
    monitor.send_msg()
