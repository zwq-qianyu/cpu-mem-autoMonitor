'''自动监控Linux服务器并发送警报消息到邮箱和微信中'''
# 需要安装 psutil 和 wechatpy
# pip3 install psutil wechatpy
import psutil, time

class monitor:
    #get the hostname
    host = psutil.users()[0].name

    @classmethod
    def mem(cls, max=65):
        used = psutil.virtual_memory().percent
        if used > max:
            #cls.mail("你的主机-'{}'内存空间已使用{}%，超过{}%，请注意!".format(cls.host, used, max))
            cls.wechat("你的主机-'{}'内存空间已使用{}%，超过{}%，请注意!".format(cls.host, used, max))
            print("你的主机-'{}'内存空间已使用{}%，超过{}%，请注意!".format(cls.host, used, max))

    @classmethod
    def cpu(cls, max=20):
        used = psutil.cpu_percent(1)   #interval is 1 second
        if used > max:
            #cls.mail("你的主机-[{}]cpu负载已达到{}%，超过{}%，请注意！".format(cls.host, used, max))
            cls.wechat("你的主机-[{}]cpu负载已达到{}%，超过{}%，请注意！".format(cls.host, used, max))
            print("你的主机-[{}]cpu负载已达到{}%，超过{}%，请注意！".format(cls.host, used, max))

    @classmethod
    def mail(cls, content):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr

        nickname = "Automatic Monitor Program"

        # sender info
        sender = "847497935@qq.com"
        password = "ccniqwgpieokbaii"

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


monitor.send_msg()
