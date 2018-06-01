import slacker
from websocket import create_connection
from websocket import WebSocketException
from websocket import WebSocketConnectionClosedException

try:
    from setting import API_KEY
except:
    raise Exception()

class Bot(object):

    def __init__(self):
        self.webapi = slacker.Slacker(API_KEY)

    def rtm_connect(self):
        reply = self.webapi.rtm.start().body
        time.sleep(1)
        self.parse_slack_login_data(reply)

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

    def rtm_read(self):
        json_data = self.websocket_safe_read()
        data = []
        if json_data != '':
            for d in json_data.split('\n'):
                data.append(json.loads(d))
            print(data)
        return data

    def send_message(self, channel, message, attachments=None, as_user=True, thread_ts=None):
        self.webapi.chat.post_message(
                channel,
                message,
                username=self.login_data['self']['name'],
                icon_url=self.bot_icon,
                icon_emoji=self.bot_emoji,
                attachments=attachments,
                as_user=as_user,
        thread_ts=thread_ts)


if __name__ == '__main__':
    bot = Bot()
    while True:
        bot.rtm_read()
