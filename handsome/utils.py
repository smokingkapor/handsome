# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import random
import string
import urllib
import urllib2
from xml.etree import ElementTree

from django.conf import settings
from django.core.mail import send_mail


def generate_str(length):
    seed = string.lowercase + string.digits
    result = []
    for i in range(length):
        result.append(random.choice(seed))
    return ''.join(result)


def send_sms(phone, content):
    """
    Send sms to the user.
    SMS service response:
        code    int        返回值为2时，表示提交成功
        smsid   string     仅当提交成功后，此字段值才有意义（消息ID）
        msg     string     提交结果描述

        code:
            0    提交失败
            2    提交成功
            400  非法ip访问
            401  帐号不能为空
            402  密码不能为空
            403  手机号码不能为空
            4030 手机号码已被列入黑名单
            404  短信内容不能为空
            405  用户名或密码不正确
            4050 账号被冻结
            4051 剩余条数不足
            4052 访问ip与备案ip不符
            406  手机格式不正确
            407  短信内容含有敏感字符
            4070 签名格式不正确
            4071 没有提交备案模板
            4072 短信内容与模板不匹配
            4073 短信内容超出长度限制
            408  同一手机号码一分钟之内发送频率超过10条，系统将冻结你的帐号


    """
    if not settings.SMS_NOTIFICATION_ENABLED:
        print '*'*50
        print 'SMS notification is disabled, print to console'
        print u'SMS to {}: {}'.format(phone, content)
        print '*'*50
    else:
        params = {
            'account': settings.SMS_SERVER_USERNAME,
            'password': settings.SMS_SERVER_PASSWORD,
            'mobile': phone,
            'content': content.encode('utf-8')
        }
        resp = urllib2.urlopen(settings.SMS_SERVER_URL,
                               urllib.urlencode(params))
        root = ElementTree.fromstring(resp.read())
        code, msg = ('', '')
        for child in root.getchildren():
            if 'code' in child.tag:
                code = child.text
            elif 'msg' in child.tag:
                msg = child.text
        if code != '2':
            # send sms error, send email to admin
            send_mail(
                u'发送短信通知出错',
                u'code:{}\nmsg:{}'.format(code, msg),
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMINS[0][1]],
                fail_silently=True
            )
