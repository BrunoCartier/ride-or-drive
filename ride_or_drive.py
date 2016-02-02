#!/usr/bin/python3
# vim: fileencoding=utf-8 tw=80 expandtab ts=4 sw=4 :

import json

import urllib.parse as parse
import urllib.request as request

from urllib.error import HTTPError

from config import SMS_USER, SMS_KEY, WEATHER_KEY

SMS_URL = 'https://smsapi.free-mobile.fr/sendmsg'
WEATHER_URL = 'http://api.wunderground.com/api/{}/hourly/q/FR/La_Rochelle.json'.format(WEATHER_KEY)
MESSAGE = 'Probabilités de pluie :\n' \
          '9h : {}% - 10h : {}% - 11h : {}%\n' \
          '17h : {}% - 18h : {}% - 19h : {}%'


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


def fetch_weather():
    req = request.Request(url=WEATHER_URL)
    out = {}
    wanted_hours = ['9', '10', '11', '17', '18', '19']

    try:
        with request.urlopen(req) as response:
            data = json.loads(response.readall().decode('utf8'))

            for hour_info in data['hourly_forecast']:
                hour = hour_info['FCTTIME']['hour']

                if hour in wanted_hours and hour not in out:
                    out[hour] = hour_info['pop']
            send_sms(MESSAGE.format(
                out['9'],
                out['10'],
                out['11'],
                out['17'],
                out['18'],
                out['19'],
            ))
    except HTTPError as e:
        send_sms('Désolé, y\' eu une erreur avec la requête... - {}'.format(e.reason))


if __name__ == '__main__':
    fetch_weather()
