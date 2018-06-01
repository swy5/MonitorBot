import os
import slacker
import time
import json
import logging
from ssl import SSLError
from websocket import create_connection
from websocket import WebSocketException
from websocket import WebSocketConnectionClosedException

logger = logging.getLogger(__name__)

try:
    from setting import API_KEY
except:
    raise Exception()


class Bot(object):

    def __init__(self):
        self.webapi = slacker.Slacker(API_KEY)
        self.username = None
        self.domain = None
        self.login_data = None
        self.websocket = None
        self.users = {}
        self.channels = {}
        self.connected = False
        self.rtm_connect()

    def rtm_connect(self):
        reply = self.webapi.rtm.start().body
        time.sleep(1)
        self.parse_slack_login_data(reply)

    def parse_channel_data(self, channel_data):
        self.channels.update({c['id']: c for c in channel_data})

    def parse_user_data(self, user_data):
        self.users.update({u['id']: u for u in user_data})

    def parse_slack_login_data(self, login_data):
        self.login_data = login_data
        self.domain = self.login_data['team']['domain']
        self.username = self.login_data['self']['name']
        self.parse_user_data(login_data['users'])
        self.parse_channel_data(login_data['channels'])
        self.parse_channel_data(login_data['groups'])
        self.parse_channel_data(login_data['ims'])

        proxy, proxy_port, no_proxy = None, None, None
        if 'http_proxy' in os.environ:
            proxy, proxy_port = os.environ['http_proxy'].split(':')
        if 'no_proxy' in os.environ:
            no_proxy = os.environ['no_proxy']

        self.websocket = create_connection(self.login_data['url'], http_proxy_host=proxy,
                                           http_proxy_port=proxy_port, http_no_proxy=no_proxy)
        self.websocket.sock.setblocking(0)

    def read_message(self):
        json_data = self.websocket_safe_read()
        data = []
        if json_data != '':
            for d in json_data.split('\n'):
                data.append(json.loads(d))

        if not len(data):
            return
        ty = data[0].get('type', None)
        ch = data[0].get('channel', None)
        ms = data[0].get('text', None)
        if type != 'message':
            return
        return {'message': ms, 'channel': ch}

    def websocket_safe_read(self):
        """Returns data if available, otherwise ''. Newlines indicate multiple messages """
        data = ''
        while True:
            try:
                data += '{0}\n'.format(self.websocket.recv())
            except WebSocketException as e:
                if isinstance(e, WebSocketConnectionClosedException):
                    logger.warning('lost websocket connection, try to reconnect now')
                else:
                    logger.warning('websocket exception: %s', e)
                self.reconnect()
            except Exception as e:
                if isinstance(e, SSLError) and e.errno == 2:
                    pass
                else:
                    logger.warning('Exception in websocket_safe_read: %s', e)
                return data.rstrip()

    def send_message(self, channel, message, attachments=None, as_user=True, thread_ts=None):
        self.webapi.chat.post_message(
            channel,
            message,
            username=self.login_data['self']['name'],
            icon_url=None,
            icon_emoji=None,
            attachments=attachments,
            as_user=as_user,
            thread_ts=thread_ts)
