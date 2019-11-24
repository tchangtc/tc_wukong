# -*- coding:utf-8 -*-
import pkgutil
from myrobot import config, logging
from myrobot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)


class Brain(object):

    def __init__(self, con):
        self.con = con
        self.plugins = self.init_plugins()

    def hasDisabled(self, name):
        if config.has('/{}/enable'.format(name)):
            if not config.get('/{}/enable'.format(name)):
                logger.info("插件 {} 已被禁用".format(name))
                return True
        return False

    def init_plugins(self):
        """
        读取所有的插件
        """
        plugins = []
        for finder, name, ispkg in pkgutil.walk_packages(['plugins']):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except Exception as e:
                logger.error(e)
                continue
            if hasattr(mod, 'Plugin') and \
                    issubclass(mod.Plugin, AbstractPlugin) and not self.hasDisabled(name):
                plugins.append(mod.Plugin(self.con))
        return plugins

    def doQuery(self, query):
        """
        响应用户的query
        """
        for plugin in self.plugins:
            if plugin.isValid(query):
                # 命中技能 #
                plugin.handle(query)
                return True
        # 未命中技能 #
        return False
