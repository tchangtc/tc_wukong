# -*- coding:utf-8 -*-
from Robot import Player, ASR, AI, utils
import TTS


class Conversation(object):

    def converse(self, fp):
        Player.play('static/beep_lo.wav', False)
        player = Player.SoxPlayer()
        asr = ASR.XunfeiASR()
        query = asr.transcribe(fp)
        utils.check_and_delete(fp)
        ai = AI.TulingRobot()
        phrase = ai.chat(query)
        print(phrase)
        tts = TTS.XunfeiTTS()
        fp = tts.get_speech(phrase)
        player.play(fp, True)