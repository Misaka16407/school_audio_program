# test_parser.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def extract_video_url():
    """静默提取视频地址，返回str或None"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")  # 禁止控制台日志
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 移除DevTools日志
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        driver.get("https://www.zjqzqx.com/wechat/television.html")
        time.sleep(3)  # 必须的等待时间
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        video_tag = soup.find('video') or soup.find('div', {'class': 'video-container'})
        
        if video_tag:
            return (
                video_tag.get('src') 
                or video_tag.find('source').get('src') 
                or video_tag.get('data-src')
            )
        return None
        
    except Exception:
        return None
    finally:
        if 'driver' in locals():
            driver.quit()

# 测试调用（实际使用时删除这部分）
if __name__ == "__main__":
    url = extract_video_url()
    # 此处仅为测试，正式脚本中不应有输出
    assert url is not None, "测试失败：未解析到地址"
    assert url.startswith(('http', '/')), f"异常地址格式：{url}"