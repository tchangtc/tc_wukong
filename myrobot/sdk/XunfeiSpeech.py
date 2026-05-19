import websocket
import hashlib
import base64
import hmac
import json
import wave
import tempfile
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

from myrobot import logging

logger = logging.getLogger(__name__)

STATUS_FIRST_FRAME = 0  # first frame flag
STATUS_CONTINUE_FRAME = 1  # middle frame flag
STATUS_LAST_FRAME = 2  # last frame flag

asrWsParam = None
gResult = ''
gPCMPath = ''


class ASR_Ws_Param(object):
    # initialize
    def __init__(self, APPID, APIKey, APISecret, AudioFile):
        # console auth info
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret

        # fixed params, no need to modify
        self.Host = "iat-api.xfyun.cn/v2/iat"
        self.HttpProto = "HTTP/1.1"
        self.HttpMethod = "GET"
        self.RequestUri = "/v2/iat"
        self.Algorithm = "hmac-sha256"
        self.url = "wss://" + self.Host + self.RequestUri

        # set test audio file
        self.AudioFile = AudioFile
        # common parameters
        self.CommonArgs = {"app_id": self.APPID}
        # business parameters (more customization options on the official website)
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin"}

    # generate url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # generate RFC1123 timestamp
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # concatenate string
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # hmac-sha256 encryption
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # combine auth params into dict
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # concatenate auth params, generate url
        url = url + '?' + urlencode(v)
        # This prints the connection URL. When referencing this demo, uncomment the above print to compare the url your code generates
        logger.debug('websocket url :', url)
        return url


class TTS_Ws_Param(object):
    # initialize
    def __init__(self, APPID, APIKey, APISecret, Text, voice_name="xiaoyan"):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # common parameters
        self.CommonArgs = {"app_id": self.APPID}
        # business parameters (more customization options on the official website)
        self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": voice_name, "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}

    # generate url
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # generate RFC1123 timestamp
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # concatenate string
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # hmac-sha256 encryption
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # combine auth params into dict
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # concatenate auth params, generate url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # This prints the connection URL. When referencing this demo, uncomment the above print to compare the url your code generates
        # print('websocket url :', url)
        return url


# ASR handle websocket message
def asr_on_message(ws, message):
    global gResult
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        if code != 0:
            errMsg = json.loads(message)["message"]
            logger.critical("xunfei-asr recognition error: sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            data = json.loads(message)["data"]["result"]["ws"]
            result = ""
            for i in data:
                for w in i["cw"]:
                    result += w["w"]
            gResult = gResult + result
            logger.info("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
    except Exception as e:
        logger.critical("xunfei-asr recognition error:", e)


# ASR handle websocket error
def asr_on_error(ws, error):
    logger.error("### error:", error)


# ASR handle websocket close
def asr_on_close(ws):
    logger.debug("### closed ###")


# ASR handle websocket connection open
def asr_on_open(ws):
    global asrWsParam

    def run(*args):
        frameSize = 1220  # audio frame size
        intervel = 0.04  # send interval (unit: s)
        status = STATUS_FIRST_FRAME  # audio status: first/middle/last frame
        with open(asrWsParam.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # end of file
                if not buf:
                    status = STATUS_LAST_FRAME
                # first frame: send with business params
                # appid must be included, only needed in first frame
                if status == STATUS_FIRST_FRAME:

                    d = {"common": asrWsParam.CommonArgs,
                         "business": asrWsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # middle frame
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # last frame
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # simulate audio sampling interval
                time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())


# handle websocket message
def tts_on_message(ws, message):
    try:
        code = json.loads(message)["code"]
        sid = json.loads(message)["sid"]
        audio = json.loads(message)["data"]["audio"]
        audio = base64.b64decode(audio)
        if code != 0:
            errMsg = json.loads(message)["message"]
            logger.error("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            with open(gTTSPath, 'ab') as f:
                f.write(audio)
    except Exception as e:
        logger.error("receive msg,but parse exception:", e)


# handle websocket error
def tts_on_error(ws, error):
    logger.error("### error:", error)


# handle websocket close
def tts_on_close(ws):
    global gTTSResult
    logger.debug("### closed ###")
    pcmdata = None
    try:
        with open(gTTSPath, 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        tmpfile = ''
        with tempfile.NamedTemporaryFile() as f:
            tmpfile = f.name
        with wave.open(tmpfile, 'wb') as wavfile:
            wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)
        gTTSResult = tmpfile
    except Exception as e:
        logger.error("XunfeiSpeech error: {}".format(e))


# handle websocket connection open
def tts_on_open(ws):
    global ttsWsParam

    def run(*args):
        intervel = 2  # wait interval for result (unit: s)

        d = {"common": ttsWsParam.CommonArgs,
             "business": ttsWsParam.BusinessArgs,
             "data": ttsWsParam.Data,
             }
        d = json.dumps(d)
        ws.send(d)
        # sleep while waiting for server to return result
        time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())


def transcribe(fpath, appid, api_key, api_secret):
    """
    iFlytek ASR
    """
    global asrWsParam, gResult
    gResult = ''
    asrWsParam = ASR_Ws_Param(appid, api_key, APISecret=api_secret, AudioFile=fpath)
    websocket.enableTrace(False)
    wsUrl = asrWsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=asr_on_message, on_error=asr_on_error, on_close=asr_on_close)
    ws.on_open = asr_on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return gResult


def synthesize(msg, voice_name="xiaoyan"):
    """
    iFlytek TTS
    """
    global ttsWsParam, gTTSPath, gTTSResult
    from myrobot import config
    xunfei = config.get('xunfei_yuyin', {})
    with tempfile.NamedTemporaryFile() as f:
        gTTSPath = f.name
    ttsWsParam = TTS_Ws_Param(APPID=xunfei.get('appid', ''),
                              APIKey=xunfei.get('api_key', ''),
                              APISecret=xunfei.get('api_secret', ''),
                              Text=msg,
                              voice_name=voice_name
                              )
    websocket.enableTrace(False)
    wsUrl = ttsWsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=tts_on_message, on_error=tts_on_error, on_close=tts_on_close)
    ws.on_open = tts_on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    return gTTSResult
