#!/usr/bin/python3
# vim: fileencoding=utf-8 tw=80 expandtab ts=4 sw=4 :

import urllib.parse as parse
import urllib.request as request

from urllib.error import HTTPError

from config import SMS_USER, SMS_KEY

SMS_URL = 'https://smsapi.free-mobile.fr/sendmsg'


def send_sms(text):
    data = parse.urlencode({
        'user': SMS_USER,
        'pass': SMS_KEY,
        'msg': text,
    })

    req = request.Request(url='{}?{}'.format(SMS_URL, data))

    try:
        with request.urlopen(req):
            print('Message sent!')
    except HTTPError as e:
        print('Issue with request: {}'.format(e.reason))
        print(e)

if __name__ == '__main__':
    send_sms('Salut, SMS depuis Python ! Yolo !')
