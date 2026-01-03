import os
import requests
import time
from google import genai
from telegram import Bot
import asyncio

# ========= Unix時間, 24小時前Unix =========
NOW_TIME = int(time.time())
TWENTYFOUR_HOUR = NOW_TIME - 86400

# ========= API & ID =========
GEMINI_API_KEY= os.getenv("AIzaSyDEEy28KlPBfNqZ2END0fQ2R0bLAsSrFQY")
TELEGRAM_BOT_TOKEN= os.getenv("8586350968:AAGAFZ3j1-dZRewdYiiI3J8liDFb-zb8v4g")
TELEGRAM_CHAT_ID= os.getenv("5515327656")

# ========= 網站, 格式過濾=========
COINDESK_URL = requests.get("https://data-api.coindesk.com/news/v1/article/list?lang=EN&limit=100&source_ids=coindesk")
COINDESK_CONTECT = COINDESK_URL.json()
COINDESK_CONTECT_DATA = COINDESK_CONTECT.get('Data',[])
LATEST_NEWS = [] # 建立空清單來存放結果

for item in COINDESK_CONTECT_DATA:
    # 擷取時間點
    pub_time = int(item.get("PUBLISHED_ON", 0))

    #篩選時間
    if pub_time >= TWENTYFOUR_HOUR:
        # 時間符合，才開始擷取其他欄位
        news_info = {
            "Time": pub_time,
            "Title": item.get("TITLE", "Null"),
            "Subtitle": item.get("SUBTITLE", "Null"),
            "Url": item.get("URL", "Null"),
            "Body": item.get("BODY", "Null"),
        }
        LATEST_NEWS.append(news_info)

# ========= YESTERDAT_NEWS,24小時前所有新聞, 格式string =========
YESTERDAT_NEWS = str(LATEST_NEWS)

# ========= 召喚Gemini =========
client = genai.Client(api_key=GEMINI_API_KEY)
contect = "Hello"             #========= 要下好Prompt(很重要!!!)，寫好Prompt之後要給AI算一下Token會不會超過免費額度 =========

resp = client.models.generate_content(
    model="gemini-2.5-flash", #目前測試有回應的模型(傻眼)...
    contents=contect,
)

# ========= 24小時前所有新聞整理總結(Gemini, 格式string) =========
gemini_response = resp.text

# ========= 召喚TGBOT, 傳出Gemini回應的資料 =========
async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN) #BOT的TOKEN_ID
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID,text=f'今日新聞:\n{gemini_response}') #CHAT_ID
asyncio.run(main())


print(YESTERDAT_NEWS) #給AI算一下Token會不會超過免費額度




