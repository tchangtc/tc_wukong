# -*- coding:utf-8 -*-
from myrobot import Player, AI, utils, ASR, TTS
from myrobot.Brain import Brain
import requests
import uuid


class Conversation(object):

    def __init__(self):
        self.history = []
        self.player = None

    def doResponse(self, query):
        self.appendHistory(0, query)
        brain = Brain(self)
        if not brain.doQuery(query):
            ai = AI.TulingRobot()
            phrase = ai.chat(query)
            self.say(phrase, True)
            print(phrase)

    def handle(self, query):
        city = 'Shanghai'
        url = 'https://free-api.heweather.net/s6/weather/forecast?parameters'
        params = {
            "location": city,
            "key": "f099fbd4c79041f9aa2c7870aab5b16b"
        }
        r = requests.get(url, params=params)
        r.encoding = 'utf-8'
        try:
            results = r.json()['HeWeather6'][0]['daily_forecast']
            res = '{} Weather:'.format(city)
            day_label = ['Today', 'Tomorrow', 'Day after tomorrow']
            i = 0
            for result in results:
                tmp_min, tmp_max, cond_txt_d, cond_txt_n = \
                    result['tmp_min'], result['tmp_max'], result['cond_txt_d'], result['cond_txt_n']
                res += '\n{}: Day {}, Night {}, Temperature {} to {} Celsius'.format(day_label[i], cond_txt_d, cond_txt_n, tmp_min, tmp_max)
                i += 1
            return res
        except Exception as e:
            print(e)
            return 'Weather query failed!'

    def converse(self, fp):
        Player.play('static/beep_lo.wav', False)
        asr = ASR.XunfeiASR()
        query = asr.transcribe(fp)
        print(query)
        self.doResponse(query)
        utils.check_and_delete(fp)

    def say(self, phrase, delete=False):
        """
        Say a sentence
        """
        self.appendHistory(1, phrase)
        self.player = Player.SoxPlayer()
        tts = TTS.XunfeiTTS()
        fp = tts.get_speech(phrase)
        self.player.play(fp, True)

    def stop(self):
        if self.player:
            self.player.stop()

    def getHistory(self):
        return self.history

    def appendHistory(self, type, text):
        if type in (0, 1) and text != '':
            self.history.append({'type': type, 'text': text, 'uuid': str(uuid.uuid1())})
