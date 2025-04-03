import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselColumn,
    MessageTemplateAction,
    PostbackAction,
    FlexSendMessage,
    BubbleContainer,
    TextComponent,
    BoxComponent,
    CarouselContainer,
    StickerMessage,
    ImageSendMessage,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    ImageComponent,
    CarouselTemplate,
    ButtonsTemplate
)

app = Flask(__name__)

# 初始化 LineBotApi 和 WebhookHandler
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@line_handler.add(FollowEvent)
def handle_follow(event: FollowEvent):
    user_id = event.source.user_id
    reply_token = event.reply_token

    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    # 歡迎訊息
    welcome_message = f"Hi！{user_name}👋\n歡迎來到煤鄉與河谷交織的秘境──猴硐\n準備好和考察隊一起出發了嗎？(●'◡'●)\n請輸入「GoGo」讓我們一起揭開猴硐的神秘面紗吧！"
    line_bot_api.reply_message(reply_token, TextSendMessage(text=welcome_message))

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    user_id = event.source.user_id
    user_input = event.message.text.strip()

    if user_input.lower() == "gogo":
        reply_token = event.reply_token
        
        # 第一個訊息：文字訊息
        text_message_1 = TextSendMessage(text="你是一名礦工，天剛破曉，你站在復興坑的礦坑口，準備開始今天的工作。工頭拍了拍你的肩膀，交給你今天的兩個任務。")

        # 第一個任務：軌道夫
        bubble_1 = BubbleContainer(
            direction='ltr',
            hero=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text="第一關　軌道夫",
                        weight="bold",  # 標題加粗
                        size="xl",
                        align="start",  # 靠左對齊
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="📍 場景",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        weight="bold",  # 加粗
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="復興坑到整煤廠之間",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="🛠 任務目標",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        weight="bold",  # 加粗
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="跟著巡視復興坑到整煤廠之間的礦車路線，檢查軌道，確認軌道破損的路段。",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        margin="md"  # 增加間距
                    )
                ],
                padding_all="20px",  # 設定內邊距
            ),
            styles={
                "body": {
                    "backgroundColor": "#F0F0F0",  # 留白背景色
                }
            }
        )

        # 第二個任務：選洗煤工
        bubble_2 = BubbleContainer(
            direction='ltr',
            hero=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(
                        text="第二關　選洗煤工",
                        weight="bold",  # 標題加粗
                        size="xl",
                        align="start",  # 靠左對齊
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="📍 場景",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        weight="bold",  # 加粗
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="整煤廠內",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="🛠 任務目標",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        weight="bold",  # 加粗
                        margin="md"  # 增加間距
                    ),
                    TextComponent(
                        text="跟著煤礦運送的路線，到整煤廠完成選煤。",
                        size="sm",
                        wrap=True,
                        align="start",  # 靠左對齊
                        margin="md"  # 增加間距
                    )
                ],
                padding_all="20px",  # 設定內邊距
            ),
            styles={
                "body": {
                    "backgroundColor": "#F0F0F0",  # 留白背景色
                }
            }
        )

        # 將兩個 Bubble 放入 Carousel 中，實現左右顯示
        carousel = CarouselContainer(
            contents=[bubble_1, bubble_2]
        )

        # 將 Carousel 包裝成 Flex 訊息
        flex_message = FlexSendMessage(
            alt_text="任務卡片",
            contents=carousel
        )

        # 第三個訊息：文字訊息
        text_message_2 = TextSendMessage(
            text="👉「在事務所的牆上有四句標語，這是礦工們必須記住的重要原則！請從右至左跟我複誦一次（中間使用空格分開）。」"
        )
        
        # 傳送三個訊息：文字訊息 + 任務 Flex 訊息 + 文字訊息
        line_bot_api.reply_message(reply_token, [text_message_1, flex_message, text_message_2])

    elif user_input == "努力生產 安全為先 提高警覺 防患未然":
        reply_token = event.reply_token

        # 傳送後續訊息
        task_message_3 = TextSendMessage(
            text="坑道內昏暗潮濕，耳邊傳來礦車滑過鐵軌的聲音。你沿著軌道前行，準備迎接今天的第一項任務……\n🔧【軌道夫的挑戰即將開始！】"
        )
        sticker_message = StickerMessage(package_id=11539, sticker_id=52114146)

        text_message_4 = TextSendMessage(
            text="你走出了礦坑，微光透過樹梢灑落，空氣中帶著淡淡的潮濕氣息。按照礦工的習俗，離開坑道後，應當前往某個地方參拜，以感謝今日的平安歸來。然而，這座小廟隱藏在山林之間，並不是那麼容易找到。"
        )
        text_message_5 = TextSendMessage(
            text="👉「尋找這座廟，輸入它的名稱。」"
        )
        
        line_bot_api.reply_message(reply_token, [task_message_3, sticker_message, text_message_4, text_message_5])

    elif user_input == "福正宮" or user_input == "寄命土地公":
        reply_token = event.reply_token

        # 設置 FlexMessage 的內容
        bubble = BubbleContainer(
            size="giga",
            hero=ImageComponent(
                url="https://i.imgur.com/N6NqX7t.png",  # 你的圖片 URL
                size="full",
                aspect_mode="cover",  # 設置為滿版
                aspect_ratio="1:1"  # 保持圖片的比例為 1:1
            )
        )

        # 包裝為 FlexMessage
        flex_message = FlexSendMessage(
            alt_text="滿版圖片",
            contents=bubble
        )
    
        text_message_6 = TextSendMessage(
            text="在侯硐路上偶然聽到幾位長輩坐在院子前的長椅上閒聊：「這裡有別於其他公寓式的宿舍啊，是較高級的獨戶宿舍！不過未來的年輕人恐怕都不知道它的故事了……」讓人不禁想一探究竟。"
        )

        text_message_7 = TextSendMessage(
            text="🔍 建築特徵如下：\n(1) ㄇ字型建築：三面圍繞形成中庭，與一般礦工公寓不同，屬於獨戶宿舍。\n(2) 黑瓦屋頂：屋頂鋪設日本黑瓦。\n👉 「請在侯硐路上找到這棟建築，並告訴我它是什麼？」"
        )
    
        line_bot_api.reply_message(reply_token, [flex_message, text_message_6, text_message_7])

    elif user_input == "美援厝":
        reply_token = event.reply_token
        
        # 設置 FlexMessage 的內容
        bubble_2 = BubbleContainer(
            size="giga",
            hero=ImageComponent(
                url="https://i.imgur.com/Sm3IivK.png",  # 你的圖片 URL
                size="full",
                aspect_mode="cover",  # 設置為滿版
                aspect_ratio="1:1"  # 保持圖片的比例為 1:1
            )
        )

        # 包裝為 FlexMessage
        flex_message_2 = FlexSendMessage(
            alt_text="滿版圖片",
            contents=bubble_2
        )

        # 創建 ButtonsTemplate，包含是/否選項
        buttons_template = ButtonsTemplate(
            title="美援厝居住狀況",  # 標題
            text="觀察美援厝，看看是否目前還有居民居住呢？",  # 顯示的文字
            actions=[
                MessageTemplateAction(
                    label="是",  # 按鈕顯示文字
                    text="是"  # 用戶按下按鈕後發送的訊息
                ),
                MessageTemplateAction(
                    label="否",  # 按鈕顯示文字
                    text="否"  # 用戶按下按鈕後發送的訊息
                ),
            ]
        )
        
        # 包裝成 TemplateMessage
        template_message = TemplateSendMessage(
            alt_text="美援厝居住狀況選擇",  # 替代文字
            template=buttons_template  # 按鈕模板
        )

        # 發送選擇訊息
        line_bot_api.reply_message(reply_token, [flex_message_2, template_message])

    elif user_input == "是":
        # 在這裡添加「是」選項的回應邏輯，並繼續下一步

        messages = [
            TextSendMessage(text = "雖然礦業時代已成過去，美援厝仍有居民居住，繼續見證著這段歷史。下次經過，不妨留意屋簷下聊天的長輩們，或許他們還能分享更多關於猴硐的故事呢！ 😊"),
            TextSendMessage(text = "還記得剛才在美援厝前的院子，有位長輩說到「當年我兒子可是王醫生接生的呢！當時許多地方居民半夜生病，前往王醫生家緊急敲門求救，不管多晚王醫生皆會立刻前往診治，真是我們瑞三礦工們的菩薩啊……不知道去那棟石砌牆構造的房屋還找不找的到他？」聽完這段讓人不禁想知道這位醫生的故事。"),
            TextSendMessage(text = "👉「請在侯硐路上找到一棟石砌牆構造的房屋，並告訴我他是什麼？」")
        ]

        line_bot_api.reply_message(event.reply_token, messages)
        
        # 這裡可以繼續發送更多訊息或進行下一步的邏輯

    elif user_input == "否":
        # 在這裡添加「否」選項的回應邏輯，重新跳出選項框
        reply_token = event.reply_token
        
        # 重新顯示選擇框，進行迴圈
        buttons_template = ButtonsTemplate(
            title="美援厝居住狀況",  # 標題
            text="觀察美援厝，看看是否目前還有居民居住呢？",  # 顯示的文字
            actions=[
                MessageTemplateAction(
                    label="是",  # 按鈕顯示文字
                    text="是"  # 用戶按下按鈕後發送的訊息
                ),
                MessageTemplateAction(
                    label="否",  # 按鈕顯示文字
                    text="否"  # 用戶按下按鈕後發送的訊息
                ),
            ]
        )
        
        # 包裝成 TemplateMessage
        template_message = TemplateSendMessage(
            alt_text="美援厝居住狀況選擇",  # 替代文字
            template=buttons_template  # 按鈕模板
        )

        # 重新發送選擇訊息
        line_bot_api.reply_message(reply_token, template_message)

    elif user_input == "醫護所" or user_input == "員工診所" :
        reply_token = event.reply_token
        text_message_8 = TextSendMessage(
            text="沒錯，這裡正是醫護所。但是長輩們想尋找的王醫生仔，沒人記得他的全名了🥲，請協助長輩透過搜尋引擎查找瑞三醫護所的醫生，找出他的全名。"
        )
        line_bot_api.reply_message(reply_token, text_message_8)
        
    elif user_input == "王則能":
        reply_token = event.reply_token
        text_message_9 = TextSendMessage(
            text="長輩轉過身來，滿懷感激地看著你，眼中閃爍著回憶與感動🫡：\n「年輕人，真的謝謝你幫我們找到王醫生的名字……我們這些老礦工，年紀大了，很多事都慢慢忘了，可是王醫生對我們的恩情，一輩子都不會忘。」\n\n👉輸入「太好了」回應長輩並進入下個場景"
        )

        # 設置 FlexMessage 的內容
        bubble = BubbleContainer(
            size="giga",
            hero=ImageComponent(
                url="https://i.imgur.com/reutJlu.png",  # 你的圖片 URL
                size="full",
                aspect_mode="cover",  # 設置為滿版
                aspect_ratio="1:1"  # 保持圖片的比例為 1:1
            )
        )

        # 包裝為 FlexMessage
        flex_message_3 = FlexSendMessage(
            alt_text="滿版圖片",
            contents=bubble
        )

        line_bot_api.reply_message(reply_token, [text_message_9, flex_message_3])

    elif user_input == "太好了":
        reply_token = event.reply_token

        text_message_10 = TextSendMessage(
            text="看到連接整煤廠的大橋了嗎？這座運煤橋可是昭和17年（1942）配合火車通車就興建完成開始使用囉，最早是三層樓高的鐵橋。運煤橋橫跨基隆河，又稱「三層鐵橋」。不過1960年代後將原本的三層鐵橋使用鋼筋混泥土改建為圓弧形拱橋，並命名為「瑞三大橋」。"
            )
        image_1 = ImageSendMessage(original_content_url='https://i.imgur.com/VLb1OJt.jpg', preview_image_url='https://i.imgur.com/VLb1OJt.jpg')
        
        buttons_template = ButtonsTemplate(
            title="場景：運煤橋",  # 標題
            text="👉「這張照片是日本時代的三層鐵橋，在橋下觀察現在的瑞三大橋，看看三層鐵橋有哪些部分目前還保留著呢？」",  # 顯示的文字
            actions=[
                MessageTemplateAction(
                    label="橋墩",  # 按鈕顯示文字
                    text="橋墩"  # 用戶按下按鈕後發送的訊息
                ),
                MessageTemplateAction(
                    label="下弦構材",  # 按鈕顯示文字
                    text="下弦構材"  # 用戶按下按鈕後發送的訊息
                ),
                MessageTemplateAction(
                    label="橫樑",  # 按鈕顯示文字
                    text="橫樑"  # 用戶按下按鈕後發送的訊息
                ),
            ]
        )
        
        # 包裝成 TemplateMessage
        template_message_2 = TemplateSendMessage(
            alt_text="問題選擇",  # 替代文字
            template=buttons_template  # 按鈕模板
        )

        # 發送選擇訊息
        line_bot_api.reply_message(reply_token, [text_message_10, image_1, template_message_2])


    elif user_input == "橋墩":
        # 用戶選擇「橋墩」後的回應（正確答案）
        messages_2 = TextSendMessage(text="✅ 正確！當年改建成鋼筋混凝土的拱橋，靠河岸兩側的兩座橋梁仍保留日本時代的三層鐵橋的橋墩呢。")
        image_2 = ImageSendMessage(original_content_url='https://i.imgur.com/13J0xY1.jpg', preview_image_url='https://i.imgur.com/13J0xY1.jpg')
        image_3 = ImageSendMessage(original_content_url='https://i.imgur.com/lyM8M7R.png', preview_image_url='https://i.imgur.com/lyM8M7R.png')
        messages_3 = TextSendMessage(text="「這是1980年代的運煤橋，面對猴硐坑的方向，與今日對比，是不是旁邊多了輸送帶呢！跟著這張周朝南提供，簡紫吟改繪的地圖，尋找看看輸送帶最遠處的山上是甚麼空間吧。」")

        line_bot_api.reply_message(event.reply_token, [messages_2, image_2, image_3, messages_3])


    elif user_input == "下弦構材" or user_input == "橫樑":
        # 用戶選擇「下弦構材」或「橫樑」後的回應（錯誤答案）
        line_bot_api.reply_message(event.reply_token, [
            TextSendMessage(text="❌ 不是哦，這個部分在瑞三大橋中並未保留。"),
            TextSendMessage(text="請重新選擇，這是你的選項："),
            TemplateSendMessage(
                alt_text="重新選擇",
                template=ButtonsTemplate(
                    title="場景：運煤橋",  # 標題
                    text="👉「這張照片是日本時代的三層鐵橋，在橋下觀察現在的瑞三大橋，看看三層鐵橋有哪些部分目前還保留著呢？」",  # 顯示的文字
                    actions=[
                        MessageTemplateAction(
                            label="橋墩",  # 按鈕顯示文字
                            text="橋墩"  # 用戶按下按鈕後發送的訊息
                        ),
                        MessageTemplateAction(
                            label="下弦構材",  # 按鈕顯示文字
                            text="下弦構材"  # 用戶按下按鈕後發送的訊息
                        ),
                        MessageTemplateAction(
                            label="橫樑",  # 按鈕顯示文字
                            text="橫樑"  # 用戶按下按鈕後發送的訊息
                        ),
                    ]
                )
            )
        ])

    elif user_input == "捨石場" or user_input == "員工診所" :
        reply_token = event.reply_token
        text_message_11 = TextSendMessage(
            text="沒錯！輸送帶連接的是捨石場，將整煤廠剩下的煤渣跟石頭輸送至山上捨石場廢棄。"
            )
        text_message_12 = TextSendMessage(
            text="🔧 恭喜完成軌道夫的挑戰！工頭拍拍你的肩膀，滿意地點點頭：「不錯嘛，小子，這條軌道今天沒問題，礦車可以順利通行！」"
            )
        text_message_13 = TextSendMessage(
            text="👉「可以前往整煤廠參觀了解選煤的操作步驟唷！」\n(自導式考察到此結束，感謝參與🫡)"
        )
        line_bot_api.reply_message(reply_token, [text_message_11, text_message_12, text_message_13])

    else:
        reply_token = event.reply_token
        text_messages = TextSendMessage(text="不對哦！再想想看")
        line_bot_api.reply_message(reply_token, text_messages)

    


if __name__ == "__main__":
    app.run()
