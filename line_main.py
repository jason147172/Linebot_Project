from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent,
    ImageMessage, PostbackEvent
)

app = Flask(__name__)

line_bot_api = LineBotApi('aPCGG+lKJZsnLqCmtq844P8hHjQgPjtJMd8ipl+tBFhlVcq4hMxtD+lahLGtpfvl+AFCFCgjJECU3et9BS9AEJWVYKOpfovqCJkgFq9kcdFRrJmFXD7PeJOVtWsqtj3f0PhbVoOmII+ygDkZQs10ZAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6f5ef4db5799c63014bc23857f3e219f')
MAIN_RICH_MENU_ID="richmenu-6c2a754c537b151002cafb1d38cc84a2"
SUB_RICH_MENU_ID="richmenu-dc78dec09ac366e9aba0ca6b4024c087"

@app.route("/callback", methods=['POST'])
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    follow_text_message = TextSendMessage("HI! 歡迎使用~")

    line_bot_api.reply_message(
        event.reply_token, follow_text_message
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_id = event.message.id

    image_id_text_send_message = TextSendMessage(text='(╯°□°）╯︵ ┻━┻')

    line_bot_api.reply_message(event.reply_token, image_id_text_send_message)
    content_file = line_bot_api.get_message_content(message_id=message_id)

    with open(message_id + '.jpg', 'wb') as tempfile:
        for chunk in content_file.iter_content():
            tempfile.write(chunk)
    
    line_bot_api.link_rich_menu_to_user(
    user_id='Uddf9fef08390be103dd04930adc57884',
    rich_menu_id=SUB_RICH_MENU_ID
    )

@handler.add(PostbackEvent)
def handle_postback(event):
    ts = event.postback.data
    if ts == "action=back":
            line_bot_api.link_rich_menu_to_user(
            user_id='Uddf9fef08390be103dd04930adc57884',
            rich_menu_id=MAIN_RICH_MENU_ID
            )


if __name__ == "__main__":
    app.run()

