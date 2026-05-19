import tornado.ioloop
import tornado.web
import tornado.escape
import threading
import asyncio
import sys
from myrobot import config
import json

conversation = None


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('user')


class MainHandler(BaseHandler):
    global conversation

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        # self.render('index.html')
        self.render('index.html', history=conversation.getHistory())


class LogHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render('log.html')


class HistoryHandler(BaseHandler):

    def get(self):
        global conversation
        if not self.current_user:
            res = {'code': 1, 'message': 'illegal visit'}
        else:
            res = {'code': 0, 'message': 'ok', 'history': json.dumps(conversation.getHistory())}
        self.write(json.dumps(res))
        self.finish()


class ChatHandler(BaseHandler):

    def post(self):
        global conversation
        if not self.current_user:
            res = {'code': 1, 'message': 'illegal visit'}
        else:
            query = self.get_argument('query', '')
            if query != '':
                conversation.doResponse(query)
            res = {'code': 0, 'message': 'ok'}
        self.write(json.dumps(res))
        self.finish()


class ConfigHandler(BaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/login")
            return
        self.render('config.html')


class LoginHandler(BaseHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
            return
        # self.write('<html><body><form action="/login" method="post">'
        #            'Name: <input type="text" name="name"><br/>'
        #            'Password: <input type="password" name="password">'
        #            '<input type="submit" value="Sign in">'
        #            '</form></body></html>')
        self.render('login.html')

    def post(self):
        if config.get('/server/password') == self.get_argument('password', default='') and \
                config.get('/server/name') == self.get_argument('name', default=''):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.write('Login failed!')


settings = {
    "cookie_secret": config.get('/server/cookie_secret', 'change_me_to_a_random_string'),
    "template_path": "server/template",
    "static_path": "server/static"

}


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/config", ConfigHandler),
        (r"/log", LogHandler),
        (r"/history", HistoryHandler),
        (r"/chat", ChatHandler)
    ], **settings)


app = make_app()


def start_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.listen(config.get('/server/port', 5000))
    tornado.ioloop.IOLoop.current().start()


def run(con):
    global conversation
    conversation = con
    threading.Thread(target=start_server).start()
