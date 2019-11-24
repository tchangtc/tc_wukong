from myrobot.sdk.AbstractPlugin import AbstractPlugin
import requests
from myrobot import logging

logger = logging.getLogger(__name__)


class Plugin(AbstractPlugin):

    def handle(self, query):
        city = '上海'
        url = 'https://free-api.heweather.net/s6/weather/forecast?parameters'
        params = {
            "location": city,
            "key": "f099fbd4c79041f9aa2c7870aab5b16b"
        }
        r = requests.get(url, params=params)
        r.encoding = 'utf-8'
        try:
            results = r.json()['HeWeather6'][0]['daily_forecast']
            res = '{} :'.format(city)
            day_label = ['今天', '明天', '后天']
            i = 0
            for result in results:
                tmp_min, tmp_max, cond_txt_d, cond_txt_n = \
                    result['tmp_min'], result['tmp_max'], result['cond_txt_d'], result['cond_txt_n']
                res += '\n{}: 白天{}, 夜间{}, 气温{}到{}摄氏度'.format(day_label[i], cond_txt_d, cond_txt_n, tmp_min, tmp_max)
                i += 1
            self.con.say(res, True)
            logger.info(res)
        except Exception as e:
            logger.error(e)
            self.con.say('天气查询失败！', True)

    def isValid(self, query):
        return '天气' in query
