# -*- coding:utf-8 -*-
import yaml
from myrobot import constant, logging

logger = logging.getLogger(__name__)

_config = {}
has_init = False


def init():
    global _config, has_init
    with open(constant.CONFIG_PATH, 'r') as f:
        _config = yaml.safe_load(f)
    has_init = True


def get_path(items, default=None):
    global _config
    curConfig = _config
    if isinstance(items, str) and items[0] == '/':
        items = items.split('/')[1:]
    for key in items:
        if key in curConfig:
            curConfig = curConfig[key]
        else:
            logger.warning('Config {} not found, using default value {}'.format('/'.join(items), default))
            return default
    return curConfig


def has_path(items):
    global _config
    curConfig = _config
    if isinstance(items, str) and items[0] == '/':
        items = items.split('/')[1:]
    for key in items:
        if key in curConfig:
            curConfig = curConfig[key]
        else:
            return False
    return True


def get(item, default=None):
    """
    Get a config value

    :param item: config key. For nested config, use '/a/b' or ['a', 'b']
    :param default: default value (optional)
    :return: the config value. If not found, returns the default value
    """
    global _config, has_init
    if not has_init:
        init()
    if not item:
        return _config
    return get_path(item, default)


def has(item):
    """
    Check if a config exists

    :param item: config key. For nested config, use '/a/b' or ['a', 'b']
    :param default: default value (optional)
    :return: whether this config exists
    """
    global _config, has_init
    if not has_init:
        init()
    return has_path(item)