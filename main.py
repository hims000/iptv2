from playwright.sync_api import sync_playwright
import time

CHANNELS = {
    "cctv1":  "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=11200132825562653886",
    "cctv2":  "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=12030532124776958103",
    "cctv4":  "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=10620168294224708952",
    "cctv7":  "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=8516529981177953694",
    "cctv9":  "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=7252237247689203957",
    "cctv10": "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=14589146016461298119",
    "cctv12": "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=13180385922471124325",
    "cctv13": "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=16265686808730585228",
    "cctv17": "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=4496917190172866934",
    "cctv4k": "https://m-live.cctvnews.cctv.com/live/landscape.html?liveRoomNumber=2127841942201075403",
}

def grab(name, url):
    result = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(
            user_agent="Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 Chrome/115.0.0.0 Mobile Safari/537.36",
            viewport={"width": 360, "height": 640},
            is_mobile=True
        ).new_page()

        page.on("request", lambda req: (globals().__setitem__("result", req.url) or None) if ".m3u8" in req.url and not result else None)

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            page.evaluate("document.querySelector('video')?.play()")
            for _ in range(30):
                if result: break
                time.sleep(1)
        except:
            pass
        browser.close()
    return name, result

results = [grab(n, u) for n, u in CHANNELS.items()]

with open("live.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for name, url in results:
        if url:
            f.write(f"#EXTINF:-1,{name}\n{url}\n")
