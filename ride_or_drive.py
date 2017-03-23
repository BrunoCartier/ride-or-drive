#!/usr/bin/python3
# vim: fileencoding=utf-8 tw=80 expandtab ts=4 sw=4 :

import json

import urllib.parse as parse
import urllib.request as request

from urllib.error import HTTPError

from config import SMS_USER, SMS_KEY, WEATHER_KEY

SMS_URL = 'https://smsapi.free-mobile.fr/sendmsg'
WEATHER_URL = 'http://api.wunderground.com/api/{}/hourly/q/FR/zmw:00000.1.07316.json'.format(WEATHER_KEY)
MESSAGE = 'Probabilités de pluie :\n' \
          '{}, {}, {}\n' \
          '{}, {}, {}\n\n' \
          'Donc, matin={}%, aprèm={}%.\n\n' \
          '{}'
INSTRUCTIONS = [
    'Laisse la voiture, il y a peu de chances qu\'il pleuve :D',
    'Quelques chances de pluie. Tu peux y aller, mais attention :o',
    'Wotch, y\'a pas mal de chances pour que ça pleuve. Voiture conseillée :/',
]
THRESHOLDS = [33, 50]
WANTED_HOURS = ['8', '9', '10', '16', '17', '18']


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

    try:
        with request.urlopen(req) as response:
            data = json.loads(response.readall().decode('utf8'))

            for hour_info in data['hourly_forecast']:
                hour = hour_info['FCTTIME']['hour']

                if hour in WANTED_HOURS and hour not in out:
                    out[hour] = hour_info['pop']

            return out
    except HTTPError as e:
        send_sms('Désolé, y\' eu une erreur avec la requête... - {}'.format(e.reason))
        return


def send_weather(weather):
    def make_percentage(hour):
        return '{}h={}%'.format(
            hour,
            weather[hour]
        )

    morning = [
        int(weather[WANTED_HOURS[0]]),
        int(weather[WANTED_HOURS[1]]),
        int(weather[WANTED_HOURS[2]]),
    ]
    morning_average = round(sum(morning) / len(morning), 2)

    evening = [
        int(weather[WANTED_HOURS[3]]),
        int(weather[WANTED_HOURS[4]]),
        int(weather[WANTED_HOURS[5]]),
    ]
    evening_average = round(sum(evening) / len(evening), 2)

    max_probability = max(morning_average, evening_average)
    if max_probability < THRESHOLDS[0]:
        instruction = INSTRUCTIONS[0]
    elif max_probability < THRESHOLDS[1]:
        instruction = INSTRUCTIONS[1]
    else:
        instruction = INSTRUCTIONS[2]

    send_sms(MESSAGE.format(
        make_percentage(WANTED_HOURS[0]),
        make_percentage(WANTED_HOURS[1]),
        make_percentage(WANTED_HOURS[2]),
        make_percentage(WANTED_HOURS[3]),
        make_percentage(WANTED_HOURS[4]),
        make_percentage(WANTED_HOURS[5]),
        morning_average,
        evening_average,
        instruction,
    ))


if __name__ == '__main__':
    send_weather(fetch_weather())
