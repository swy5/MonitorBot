## Monitor Bot

### できること
1. Pythonスクリプト内に, あなたのSlackチャンネルへメッセージを送る機能を忍ばせられます.
1. メッセージ以外にも, Matplotlibで作成したグラフ画像や, PillowのImageも送ることができます.
1. Slackから実行中のPythonスクリプト内の関数をキックするように, BOTに命令できます.

具体的に下のような感じです.

##### 1. Pythonスクリプト内に, あなたのSlackチャンネルへメッセージを送る機能を忍ばせられます.
<img src="static/m1.png">
<img src="static/m2.png">

##### 2. メッセージ以外にも, Matplotlibで作成したグラフ画像や, PillowのImageも送ることができます.
<img src="static/m3.png">
<img src="static/m4.png">

##### 3. Slackから実行中のPythonスクリプト内の関数をキックするように, BOTに命令できます.
<img src="static/m5.png">
<img src="static/m6.png">

## 使い方
最初にSlack Botのアカウントを作成する必要があります.  
以下のwebサイトを参考に, Botアカウントの作成とAPIトークンの取得を行ってください.

- Pythonを使ったSlackBotの作成方法(https://qiita.com/kunitaya/items/690028e33ba5c666f3e2)
- API トークンの生成と再生成(https://get.slack.help/hc/ja/articles/215770388-API-%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E7%94%9F%E6%88%90%E3%81%A8%E5%86%8D%E7%94%9F%E6%88%90)

APIトークンを取得できたら, 環境変数にAPIトークンを設定してください.  
環境変数名は `BOT_KEY` としてください.

Linux, MAC:  
`export BOT_KEY=set_your_api_tokenxxxxxxxxxxxxxxxxxxxxxxxxxx`

Windows:  
http://www.k-cube.co.jp/wakaba/server/environ.html

### モジュールのロード&インスタンス化
環境変数BOT_KEYが適切に設定されていれば, 以下のコードで
Botを使用する準備ができます.

```
from monitor_bot.bot import MonitorBot
bot = MonitorBot()
```
