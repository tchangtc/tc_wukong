# -*- coding: utf-8-*-
import os
import shutil

CONFIG_PATH = 'config.yml'
LOGGING_PATH = 'wukong.log'


# Wukong main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

LIB_PATH = os.path.join(APP_PATH, "robot")
DATA_PATH = os.path.join(APP_PATH, "static")
TEMP_PATH = os.path.join(APP_PATH, "temp")
TEMPLATE_PATH = os.path.join(APP_PATH, "server", "templates")
PLUGIN_PATH = os.path.join(APP_PATH, "plugins")
DEFAULT_CONFIG_NAME = 'default.yml'
CUSTOM_CONFIG_NAME = 'config.yml'

# CONFIG_PATH = os.path.expanduser(
#     os.getenv('WUKONG_CONFIG', '~/.wukong')
# )
CONTRIB_PATH = os.path.expanduser(
    os.getenv('WUKONG_CONFIG', '~/.wukong/contrib')
)
CUSTOM_PATH = os.path.expanduser(
    os.getenv('WUKONG_CONFIG', '~/.wukong/custom')
)


def getConfigPath():
    """
    Get the config file path

    returns: config file storage path
    """
    return os.path.join(CONFIG_PATH, CUSTOM_CONFIG_NAME)


def getQAPath():
    """
    Get the QA dataset file path

    returns: QA dataset file storage path
    """
    qa_source = os.path.join(DATA_PATH, 'qa.csv')
    qa_dst = os.path.join(CONFIG_PATH, 'qa.csv')
    if not os.path.exists(qa_dst):
        shutil.copyfile(qa_source, qa_dst)
    return qa_dst


def getConfigData(*fname):
    """
    Get the path of a specified file in the config directory

    :param *fname: file name(s). If multiple, they are auto-joined
    :returns: file storage path under the config directory
    """
    return os.path.join(CONFIG_PATH, *fname)


def getData(*fname):
    """
    Get the path of a specified file in the resource directory

    :param *fname: file name(s). If multiple, they are auto-joined
    :returns: file storage path
    """
    return os.path.join(DATA_PATH, *fname)


def getDefaultConfigPath():
    return getData(DEFAULT_CONFIG_NAME)


def newConfig():
    shutil.copyfile(getDefaultConfigPath(), getConfigPath())


def getHotwordModel(fname):
    if os.path.exists(getData(fname)):
        return getData(fname)
    else:
        return getConfigData(fname)


