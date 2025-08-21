# termux_test.py
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # Termux 推荐 Firefox
from bs4 import BeautifulSoup
import time

def extract_video_url():
    """Termux 专用静默解析（返回视频地址或None）"""
    try:
        # 1. 配置 Firefox 无头模式（Termux 兼容性最佳）
        options = Options()
        options.add_argument("--headless")
        options.set_preference("dom.webnotifications.enabled", False)
        
        # 2. 启动 Geckodriver（需提前安装）
        driver = webdriver.Firefox(options=options)
        
        # 3. 访问页面并等待
        driver.get("https://www.zjqzqx.com/wechat/television.html")
        time.sleep(5)  # Termux 性能较低，需更长等待
        
        # 4. 解析视频地址
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_tag = soup.find('video') or soup.find('div', class_='video-wrapper')
        
        if video_tag:
            return (
                video_tag.get('src') 
                or getattr(video_tag.find('source'), 'get', lambda _: None)('src')
            )
        return None
        
    except Exception as e:
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

# 测试调用
if __name__ == "__main__":
    url = extract_video_url()
    # 此处仅为验证，正式使用时应删除
    assert url, "解析失败：返回值为空"