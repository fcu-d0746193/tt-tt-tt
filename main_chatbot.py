import os
from datetime import datetime
import workout_select
import workout_crawler
import configparser



from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)


#config = configparser.ConfigParser()
#config.read('config.ini')
#line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
#handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))

status1 = 0
status2 = 0
status3 = 0
status4 = 0
num = 0
imput = ""
page = 1

@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    user_id = event.source.user_id
    global status
    global status1
    global status2
    global status3
    global status4
    global flag
    global food_type
    global num
    global input
    global page
    global receive
    global food,tag

    if get_message == "飲食" or status3 != 0:
        if get_message == "飲食":
            reply3 = workout_select.select_food(get_message,status3,num) #status
            #print("****")#print(status2)
            line_bot_api.reply_message(event.reply_token,reply3)
            status3 = 1
        elif status3 == 1:
            if get_message == "早餐" or get_message == "午餐" or get_message == "晚餐" :#時段
                eat_time = get_message
                reply3 = workout_select.select_food(get_message,status3,num) #status
                line_bot_api.reply_message(event.reply_token,reply3)
                print("??????")
                status3 = 2
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入參數錯誤，請重新選擇功能"))
                status3 = 0
                eat_time = ""
        elif status3 == 2 :#選擇菜單
            if get_message == "低熱量" or get_message == "高蛋白" :
                input = get_message
                #爬資料儲存後再印出
                if num == 0 :
                    receive = workout_crawler.cra(input,num,page)
                print("Sdfsdfsdfsdffsdfsdfsdfdfsdfsdfsdfsdfsdfsdfsdfsfsfs")
                print(receive)
                reply3 = workout_select.select_food(receive,status3,num) #status
                #print(reply3)
                print(type(reply3))
                line_bot_api.reply_message(event.reply_token,reply3)
                print("SIFJLDJLSDJLSD")
                food_type = get_message
                #status3 = 0 #3
            elif get_message == "更多菜單":
                num = num + 3
                if num >= 15:
                    print("!!!!!!!!!!")
                    print(input)
                    page = page + 1
                    print("!!!!!!!!!!!!!!!!!@!@@@@@@@@@@@@@@@@@@@@")
                    print(page)
                    receive = workout_crawler.cra(input,num,page)
                    num = 0
                reply3 = workout_select.select_food(receive,status3,num) #status
                line_bot_api.reply_message(event.reply_token,reply3)
                status3 = 2
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入參數錯誤，請重新選擇功能"))
                status3 = 0
                eat_time = ""
                food_type = ""
    else : 
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "任意選擇一項功能吧"))


#if __name__ == "__main__":
#    app.run()
