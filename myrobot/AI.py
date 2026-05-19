# -*- coding: utf-8 -*-
import requests
import json
from uuid import getnode as get_mac
from myrobot import config


class AbstractRobot(object):

    def chat(self, query):
        pass


class TulingRobot(AbstractRobot):
    """
    Tuling Robot
    """

    SLUG = 'tuling-Robot'

    def __init__(self):
        self.api_key = config.get('/tuling/api_key', '')

    def chat(self, query):
        """
        Chat with Tuling robot
        """

        URL = "http://openapi.tuling123.com/openapi/api/v2"
        params = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": query
                }
            },
            "userInfo": {
                "apiKey": self.api_key,
                "userId": str(get_mac())[:32]
            }
        }
        r = requests.post(URL, data=json.dumps(params))
        r.encoding = 'utf-8'
        res = r.json()
        try:
            results = res['results']
            for result in results:
                if result['resultType'] == 'text':
                    return result['values']['text']
            return ''
        except Exception as e:
            print(e)
            return ''
