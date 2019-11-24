from snowboy import snowboydecoder
from myrobot import Player, config, logging
from server import server
from myrobot.Conversation import Conversation
import signal

logger = logging.getLogger(__name__)

interrupted = False
conversation = None


def audioRecorderCallback(fname):
    conversation.converse(fname)


# global player
# Player.play('static/beep_lo.wav', False)
# player = Player.SoxPlayer()
# asr = ASR. XunfeiASR()
# print(asr.transcribe(fname))
# print(asr.transcribe(fname))
# tts = TTS.XunfeiTTS()
# phrase = '我是齐天大圣孙悟空'
# fname = tts.get_speech(phrase)
# player.play(fname, True)

def detectedCallback():
    global conversation
    if conversation:
        conversation.stop()
    Player.play('static/beep_hi.wav', False)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


conversation = Conversation()
server.run(conversation)


model = config.get('/snowboy/hotword', 'snowboy/resources/wukong_tc.pmdl')

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=config.get('/snowboy/sensitivity', 0.38))
logger.info('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=detectedCallback,
               audio_recorder_callback=audioRecorderCallback,
               interrupt_check=interrupt_callback,
               sleep_time=0.01)

detector.terminate()
