import os
import re
import time
import json
import logging
import threading
from ssl import SSLError
from io import BytesIO
from slackclient import SlackClient
from websocket import WebSocketConnectionClosedException

from .setting import API_KEY


class MonitorBot(object):
    """
    Monitor bot class.
    Please set slack API KEY to your environment variable as following example.

    ```export BOT_KEY=xxxxxxxxxxxxxxxx```

    """

    def __init__(self):
        self.sc = SlackClient(API_KEY)
        self.thread = {}
        ret = self.sc.api_call('rtm.connect')
        if ret["ok"]:
            self.bot_id = ret['self']['id']
            self.sc.rtm_connect()
        else:
            raise Exception(ret["error"])

    def send_message(self, channel, message, attachments=None):
        """
        Args:
            channel(string):
            message(string):
            attachments(list):
        """
        self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=message,
            as_user=True,
            attachments=attachments
        )

    def upload_pyplot(self, channel, pyplot_obj):
        """
        Args:
            channel:
            pyplot_obj:
        """
        buffer = BytesIO()
        pyplot_obj.savefig(buffer)
        pyplot_obj.clf()
        self.sc.api_call(
            "files.upload",
            filename="graph.png",
            channels=channel,
            file=buffer.getvalue()
        )

    def upload_pillow(self, channel, pillow_img_obj):
        """
        Args:
            channel:
            pillow_img_obj:
        """
        buffer = BytesIO()
        pillow_img_obj.save(buffer, format="png")
        self.sc.api_call(
            "files.upload",
            filename="image.png",
            channels=channel,
            file=buffer.getvalue()
        )

    def __del__(self):
        for k in self.thread.keys():
            th_dict = self.thread[k]
            th_dict['stop_event'].set()
            th_dict['thread'].join()

    def response_to(self, pattern):
        """

        Following example response to a message 'Hello' and 
        sends message 'Hola!'

        Example:
            bot = MonitorBot()
            @bot.response_to('Hello'):
            def func(message):
                bot.send_message('@user', 'Hola')

        """
        def decorator(func):
            def loop(event):
                pt = re.compile(pattern)
                while True:
                    try:
                        if event.is_set():
                            break
                        time.sleep(1)
                        message = self.sc.rtm_read()
                        for mss in message:
                            if not len(mss):
                                continue
                            type = mss["type"]
                            if type != 'message':
                                continue
                            user = mss.get("user", None)
                            if user == self.bot_id:
                                continue

                            text = mss.get("text", '')
                            if pt.match(text):
                                func(mss)
                    except WebSocketConnectionClosedException as e:
                        print('Websocket disconnected, trying to reconnect.')
                        time.sleep(1)
                        self.sc.rtm_connect()
                    except Exception as e:
                        # TODO: Handle error.
                        raise Exception("Error: {}".formta(e))

            func_name = func.__name__
            th_dict = self.thread.get(func_name, None)
            if th_dict is not None:
                # Overrides existing thread.
                th_dict['stop_event'].set()
                th_dict['thread'].join()

            event = threading.Event()
            self.thread[func_name] = {
                "thread": threading.Thread(args=(event,), target=loop),
                "stop_event": event
            }
            self.thread[func_name]['thread'].start()
            print("MonitorBot.response_to: Ready to response using function '{}'.".format(func_name))
        return decorator
