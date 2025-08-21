# weather_video_downloader.py
import requests
from datetime import datetime
import os

def download_video():
    # 1. 构造当日视频URL（根据实际日期规律调整）
    today = datetime.now().strftime("%Y%m%d")
    video_url = f"https://www.zjqzqx.com/www/服务材料/天气预报视频/{datetime.now().strftime('%Y.%m')}/{today}/{today}tv1VA0_fwzx_电视天气预报_{today}152600.mp4"
    
    # 2. 伪装浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.zjqzqx.com/'
    }
    
    # 3. 创建存储目录
    os.makedirs("videos", exist_ok=True)
    save_path = f"videos/weather_{today}.mp4"
    
    # 4. 流式下载视频
    try:
        with requests.get(video_url, headers=headers, stream=True) as r:
            r.raise_for_status()  # 检查HTTP错误
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        print(f"✅ 视频已保存到: {save_path}")
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")

if __name__ == "__main__":
    download_video()