# -*- coding:utf-8 -*-
import yaml
from Robot import constant, logging

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
            logger.warning('没有找到配置 {} ,使用默认值{}'.format('/'.join(items), default))
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
    获取某个配置值

    :param item: 配置项名。如果是多级配置，则以 ‘/a/b’ 的形式或者 ['a', 'b']
    :param default: 默认值（可选）
    :return: 这个配置的值.如果没有该配置,则提供一个默认值
    """
    global _config, has_init
    if not has_init:
        init()
    if not item:
        return _config
    return get_path(item, default)


def has(item):
    """
    判断是否有某个配置

    :param item: 配置项名。如果是多级配置，则以 ‘/a/b’ 的形式或者 ['a', 'b']
    :param default: 默认值（可选）
    :return: 是否有这个配置.
    """
    global _config, has_init
    if not has_init:
        init()
    return has_path(item)