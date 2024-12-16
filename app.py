# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('a9Bnrsm0tlU1wrEFERnw5YfGFkBo/XJDty654clEjuNE/BNKgN5HQgVrA6T8Fqy71rMCtrF4CSuB3TPjv8KEQtFB0C7ySxSdanZQEoOFn6jICkB5OF+6JIfzQYHyA1PS50PSa1ILz4uNQ2e0sRnECwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('b960aca2a175079f7c2f3649640d3874')

line_bot_api.push_message('U4492871599fb3e554d18bdb13adcdbbb', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == "推薦景點":
        carousel_template_message = TemplateSendMessage(
            alt_text="旅遊景點推薦",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        title='台北101',
                        actions=[
                            URIAction(
                                uri='https://www.taipei-101.com.tw/tw/'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='日月潭',
                        actions=[
                            URIAction(
                                uri='https://www.sunmoonlake.gov.tw/zh-tw'
                            )
                        ]
                    ),
                    CarouselColumn(
                        title='墾丁',
                        actions=[
                            URIAction(
                                uri='https://www.ktnp.gov.tw/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
