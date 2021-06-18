from flask import Flask
from linebot import LineBotApi

app = Flask(__name__)
app.config.from_object('config.LineToken')

# line_bot_api = LineBotApi('')


@app.route('/')
def hello_world():
    return app.config['CHANNEL_ACCESS_TOKEN']


if __name__ == '__main__':
    app.run()
