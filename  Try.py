# Try 1
import requests
from datetime import datetime, timedelta
import os

def generate_daily_video_url():
    # 获取当前日期（通常播报前一天天气预报）
    target_date = datetime.now() - timedelta(days=1)
    
    # 格式化日期组件
    year = target_date.strftime("%Y")
    month = target_date.strftime("%m")
    day = target_date.strftime("%d")
    ymd = target_date.strftime("%Y%m%d")
    md = target_date.strftime("%m%d")
    
    # 拼接URL（时间戳假设为153900，可根据实际调整）
    base_url = "https://www.zjqzqx.com/www/服务材料/天气预报视频"
    video_url = f"{base_url}/{year}.{month}/{ymd}/{md}tv1VA0_fwzx_电视天气预报_{ymd}153900.mp4"
    
    return video_url

def download_weather_video():
    video_url = generate_daily_video_url()
    save_path = f"weather_{datetime.now().strftime('%Y%m%d')}.mp4"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.zjqzqx.com/'
    }
    
    try:
        response = requests.get(video_url, headers=headers, stream=True, timeout=30)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"✅ 视频下载成功: {save_path}")
            return True
        else:
            print(f"❌ 视频不存在 (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ 下载失败: {str(e)}")
        return False

# 执行下载
if __name__ == "__main__":
    download_weather_video()


#Try 1-1

def try_multiple_timestamps(base_url, ymd, md):
    # 常见时间点列表（15:00-16:00间）
    time_points = ["153000", "153900", "154500", "155300"]
    
    for time_str in time_points:
        video_url = f"{base_url}/{ymd}/{md}tv1VA0_fwzx_电视天气预报_{ymd}{time_str}.mp4"
        if requests.head(video_url).status_code == 200:
            return video_url
    return None

#Try 1-2
# 根据历史数据推断当日时间（需记录历史时间）
def infer_daily_time():
    # 这里简化为返回最常见的时间
    return "153900"  # 或 "155300"，根据多数情况选择

#Try 1-3

# 尝试获取目录列表（如果服务器允许）
def find_latest_video(base_url, ymd):
    # 尝试获取目录列表（需服务器配置允许）
    dir_url = f"{base_url}/{ymd}/"
    response = requests.get(dir_url)
    
    if response.status_code == 200:
        # 解析HTML查找最新视频文件
        soup = BeautifulSoup(response.text, 'html.parser')
        videos = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.mp4')]
        if videos:
            return dir_url + videos[-1]  # 返回最新的视频
    return None