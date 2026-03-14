import os
import time
import random
import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import requests
from dotenv import load_dotenv

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 載入 .env 檔案中的環境變數
load_dotenv()

# 從環境變數中取得 Discord Webhook URL
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 從環境變數中取得時區設定，未設定則使用系統本地時區
_tz_name = os.getenv("TIMEZONE")
if _tz_name:
    try:
        LOCAL_TZ = ZoneInfo(_tz_name)
        logger.info(f"使用時區：{_tz_name}")
    except ZoneInfoNotFoundError:
        logger.warning(f"找不到時區 '{_tz_name}'，改用系統本地時區")
        LOCAL_TZ = None
else:
    LOCAL_TZ = None
    logger.info("使用系統本地時區")

def main():
    logger.info("💧 喝水提醒機器人已啟動！")
    if not WEBHOOK_URL:
        logger.warning("找不到或未設定 DISCORD_WEBHOOK_URL (.env)")
        logger.warning("請複製 .env.sample 為 .env 並且填上你的 Webhook 連結。")
         
    while True:
        now = datetime.now(LOCAL_TZ)
        
        # 判斷是否為晚上 11 點 (23:00) 到 早上 9 點 (09:00) 的不打擾時間
        if now.hour >= 23 or now.hour < 9:
            logger.info("目前為休息時間 (23:00 - 09:00)，暫停提醒。等待中...")
            # 休息時間每隔 10 分鐘檢查一次，避免一次 sleep 太久中斷後難以喚醒
            time.sleep(600)
            continue
            
        # 若在提醒時間範圍內 (09:00 - 22:59:59)
        # 設定 1 小時 +- 半小時內的隨機數 (即 30 到 90 分鐘)
        sleep_minutes = random.uniform(30.0, 90.0)
        sleep_seconds = sleep_minutes * 60
        
        # 計算下一次提醒的時間並顯示
        next_time = now.timestamp() + sleep_seconds
        next_dt = datetime.fromtimestamp(next_time, tz=LOCAL_TZ)
        logger.info(f"下一次喝水提醒安排在 {next_dt.strftime('%H:%M:%S')} (約 {sleep_minutes:.1f} 分鐘後)。")
        
        # 暫停執行到下一次提醒時間
        time.sleep(sleep_seconds)
        
        # 暫停結束後再次確認當前時間 (避免睡一覺醒來已經進入休息時間)
        now_after_sleep = datetime.now(LOCAL_TZ)
        if now_after_sleep.hour >= 23 or now_after_sleep.hour < 9:
            logger.info("提醒時間落在休息時間，本次提醒跳過。")
            continue
            
        # 若環境變數沒有 Webhook URL 則不執行發送
        if not WEBHOOK_URL:
            logger.error("無法發送提醒：請在 .env 中設定 DISCORD_WEBHOOK_URL")
            continue
            
        # 準備發送到 Discord 的訊息 (使用 Embed)
        data = {
            "username": "喝水提醒小幫手",
            "embeds": [
                {
                    "title": "喝水",
                    "description": "💧💧💧💧",
                    "color": 3447003, # 藍色
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            ]
        }
        
        try:
            response = requests.post(WEBHOOK_URL, json=data)
            response.raise_for_status() # 檢查是否有錯誤發生
            logger.info("提醒發送成功！")
        except Exception as e:
            logger.error(f"提醒發送失敗：{e}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("⏳ 喝水提醒機器人已手掌握關閉。")
