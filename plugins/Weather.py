from myrobot.sdk.AbstractPlugin import AbstractPlugin
import requests
from myrobot import logging, config

logger = logging.getLogger(__name__)


class Plugin(AbstractPlugin):

    def handle(self, query):
        city = 'Shanghai'
        url = 'https://free-api.heweather.net/s6/weather/forecast?parameters'
        params = {
            "location": city,
            "key": config.get('/Weather/key', '')
        }
        r = requests.get(url, params=params)
        r.encoding = 'utf-8'
        try:
            results = r.json()['HeWeather6'][0]['daily_forecast']
            res = '{} :'.format(city)
            day_label = ['Today', 'Tomorrow', 'Day after tomorrow']
            i = 0
            for result in results:
                tmp_min, tmp_max, cond_txt_d, cond_txt_n = \
                    result['tmp_min'], result['tmp_max'], result['cond_txt_d'], result['cond_txt_n']
                res += '\n{}: Day {}, Night {}, Temperature {} to {} Celsius'.format(day_label[i], cond_txt_d, cond_txt_n, tmp_min, tmp_max)
                i += 1
            self.con.say(res, True)
            logger.info(res)
        except Exception as e:
            logger.error(e)
            self.con.say('Weather query failed!', True)

    def isValid(self, query):
        return 'weather' in query.lower()
