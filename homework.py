import os
import time

import requests
from twilio.rest import Client


def get_status(user_id):
    params = {
        'v': '5.122',
        'access_token': os.getenv('VK_TOKEN'),
        'user_ids': user_id,
        'fields': 'online'
    }
    response = requests.post(
        'https://api.vk.com/method/users.get',
        params=params
    ).json().get('response')

    if not response:
        return 0

    return response[0]['online']


def sms_sender(sms_text):
    client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_TOKEN'))

    message = client.messages.create(
            body=sms_text,
            from_=os.getenv('NUMBER_FROM'),
            to=os.getenv('NUMBER_TO')
        )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
