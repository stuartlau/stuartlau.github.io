import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

# 配置
USER_ID = "333834011" # 需要用户修改为自己的ID
DATA_FILE = "_data/xiaohongshu.json"
DESC = "Xiaohongshu Sync Script (Playwright)"

async def sync_xhs():
    async with async_playwright() as p:
        # 使用持久化上下文以保留登录状态
        user_data_dir = os.path.expanduser("~/.xhs_playwright_data")
        context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = await context.new_page()
        
        # 拦截API响应
        posts_data = []
        
        async def handle_response(response):
            if "api/sns/web/v1/user_posted" in response.url:
                try:
                    data = await response.json()
                    if data.get("code") == 0:
                        notes = data.get("data", {}).get("notes", [])
                        for note in notes:
                            posts_data.append({
                                "note_id": note.get("note_id"),
                                "title": note.get("display_title"),
                                "cover": note.get("cover", {}).get("url_default"),
                                "likes": note.get("interact_info", {}).get("liked_count"),
                                "type": note.get("type"),
                                "url": f"https://www.xiaohongshu.com/explore/{note.get('note_id')}"
                            })
                except Exception as e:
                    print(f"Error parsing response: {e}")

        page.on("response", handle_response)
        
        print(f"Opening Xiaohongshu profile: https://www.xiaohongshu.com/user/profile/{USER_ID}")
        await page.goto(f"https://www.xiaohongshu.com/user/profile/{USER_ID}")
        
        print("Please log in if necessary. Waiting for data...")
        # 等待页面加载并模拟滚动
        for i in range(5):
            await page.mouse.wheel(0, 2000)
            await asyncio.sleep(2)
        
        # 获取详细信息（包括视频地址）
        for note in posts_data:
            if note["type"] == "video":
                print(f"Fetching playback URL for: {note['title']}")
                await page.goto(note["url"])
                await asyncio.sleep(3) # 等待加载
                # 尝试从页面JS变量中提取视频地址 (通常在 window.__INITIAL_STATE__ 中)
                try:
                    video_url = await page.evaluate("""() => {
                        const state = window.__INITIAL_STATE__;
                        if (state && state.note && state.note.noteDetailMap) {
                            const details = Object.values(state.note.noteDetailMap)[0];
                            const video = details.note.video;
                            if (video && video.media && video.media.stream && video.media.stream.h264) {
                                return video.media.stream.h264[0].masterUrl;
                            }
                        }
                        return null;
                    }""")
                    if video_url:
                        note["video_url"] = video_url
                except Exception as e:
                    print(f"Error extracting video URL: {e}")
                
        # 保存数据
        if posts_data:
            # 去重
            unique_posts = {p['note_id']: p for p in posts_data}.values()
            output = {
                "total_count": len(unique_posts),
                "notes": list(unique_posts),
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"Successfully synced {len(unique_posts)} notes to {DATA_FILE}")
        else:
            print("No data captured. Check your login status or User ID.")
            
        await context.close()

if __name__ == "__main__":
    if not os.path.exists("_data"):
        os.makedirs("_data")
    asyncio.run(sync_xhs())
