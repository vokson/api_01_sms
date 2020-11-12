import logging
import os
import sys
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

VERSION = '5.122'
BASE_URL = 'https://api.vk.com/method'

logging.basicConfig()
log = logging.getLogger('VK_SMS_APP')
log.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
log.addHandler(stdout_handler)


def get_status(user_id):
    params = {
        'v': VERSION,
        'access_token': os.getenv('VK_TOKEN'),
        'user_ids': user_id,
        'fields': 'online'
    }
    url = '{}/{}'.format(BASE_URL, 'users.get')

    try:
        response = requests.post(url, params=params)

    except requests.exceptions.RequestException:
        log.exception('Error while handling request')
        return 0

    except Exception:
        log.exception('Unknown exception')
        return 0

    else:
        json_response = response.json()

        error = json_response.get('error')
        if error:
            print(f'VK response error: {error}')
            return 0

        user_response = json_response.get('response')
        if not user_response:
            log.error('VK response error: block "respose" is missing')
            return 0

        user = user_response[0]
        if 'online' not in user:
            log.error('VK response error: "online" field is missing')
            return 0

        return user['online']


def sms_sender(client, sms_text):
    message = client.messages.create(
            body=sms_text,
            from_=os.getenv('NUMBER_FROM'),
            to=os.getenv('NUMBER_TO')
        )
    return message.sid


if __name__ == '__main__':
    log.info('Starting application')

    vk_id = input('Введите id ')
    while True:
        client = Client(
            os.getenv('TWILIO_ACCOUNT_SID'),
            os.getenv('TWILIO_TOKEN')
        )
        if get_status(vk_id) == 1:
            sms_sender(client, f'{vk_id} сейчас онлайн!')
            break

        log.info('User is not online. Try after 5 sec')
        time.sleep(5)

    log.info('Ending application')
