from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, MessageEvent, TextSendMessage, QuickReplyButton, MessageAction, QuickReply

app = Flask(__name__)
app.config.from_object('config.LineToken')

line_bot_api = LineBotApi(app.config['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(app.config['CHANNEL_SECRET'])

lang_list = ['日本語', 'English', 'メェ語']
hello_list = {'日本語': 'こんにちは', 'English': 'Hello', 'メェ語': 'メェ～(ﾌﾞﾘｯ'}


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        make_message(event.message.text)
    )


def make_message(text):

    if text == 'Hello':
        items = [QuickReplyButton(action=MessageAction(label=f"{lang}", text=f"{lang}")) for lang in lang_list]
        messages = TextSendMessage(text="言語", quick_reply=QuickReply(items=items))
        return messages
    elif text in hello_list:
        return TextMessage(text=hello_list[text])
    else:
        return TextMessage(text=text)


if __name__ == '__main__':
    app.run()
