# -*- coding: utf-8-*-
import os
import base64
import tempfile
from . import utils, config, constant
from Robot import logging
from abc import ABCMeta, abstractmethod
from .sdk import XunfeiSpeech

logger = logging.getLogger(__name__)


class AbstractTTS(object):
    """
    Generic parent class for all TTS engines
    """

    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        profile = cls.get_config()
        instance = cls(**profile)
        return instance

    @abstractmethod
    def get_speech(self, phrase):
        pass


class XunfeiTTS(AbstractTTS):
    """
    科大讯飞的语音识别API.
    """

    SLUG = "xunfei-tts"

    def __init__(self, voice='xiaoyan'):
        # super(self.__class__, self).__init__(appid, api_key, api_secret)
        self.voice_name = voice

    @classmethod
    def get_config(cls):
        # Try to get xunfei_yuyin config from config
        return config.get('xunfei_yuyin', {})

    def get_speech(self, phrase):
        return XunfeiSpeech.synthesize(phrase, self.voice_name)


def get_engine_by_slug(slug=None):
    """
    Returns:
        A TTS Engine implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("无效的 TTS slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                                                  engine.SLUG == slug, get_engines()))

    if len(selected_engines) == 0:
        raise ValueError("错误：找不到名为 {} 的 TTS 引擎".format(slug))
    else:
        if len(selected_engines) > 1:
            logger.warning("注意: 有多个 TTS 名称与指定的引擎名 {} 匹配").format(slug)
        engine = selected_engines[0]
        logger.info("使用 {} TTS 引擎".format(engine.SLUG))
        return engine.get_instance()


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses

    return [engine for engine in
            list(get_subclasses(AbstractTTS))
            if hasattr(engine, 'SLUG') and engine.SLUG]
