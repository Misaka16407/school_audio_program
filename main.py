import requests
import os
import time
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("weather_download.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class WeatherVideoDownloader:
    def __init__(self):
        self.base_url = "https://www.zjqzqx.com/www/服务材料/天气预报视频"
        self.success_log = "success_times.csv"
        self.fallback_times = ["153400", "155300", "153900", "135000", "155900"]
        
        # 确保日志文件存在
        if not os.path.exists(self.success_log):
            with open(self.success_log, "w", encoding='utf-8') as f:
                f.write("date,success_time\n")
    
    def get_target_date(self):
        """获取目标日期（通常是前一天）"""
        return datetime.now()
    
    def get_most_recent_success_time(self):
        """从日志中获取最近成功的时间戳"""
        try:
            with open(self.success_log, "r", encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) > 1:  # 跳过标题行
                    # 获取最后一行的时间戳
                    last_line = lines[-1].strip()
                    if last_line and ',' in last_line:
                        return last_line.split(',')[1]
        except Exception as e:
            logging.error(f"读取成功日志失败: {e}")
        
        # 默认返回最近出现最多的时间戳
        return "153400"
    
    def update_success_log(self, timestamp):
        """更新成功日志"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        try:
            with open(self.success_log, "a", encoding='utf-8') as f:
                f.write(f"{date_str},{timestamp}\n")
            logging.info(f"已更新成功日志: {date_str} - {timestamp}")
        except Exception as e:
            logging.error(f"更新成功日志失败: {e}")
    
    def generate_video_urls(self):
        """生成所有可能的视频URL"""
        target_date = self.get_target_date()
        
        # 格式化日期组件
        year = target_date.strftime("%Y")
        month = target_date.strftime("%m")
        day = target_date.strftime("%d")
        ymd = target_date.strftime("%Y%m%d")
        md = target_date.strftime("%m%d")
        
        # 获取首选时间戳
        primary_time = self.get_most_recent_success_time()
        
        # 生成URL列表
        urls = []
        
        # 首选URL
        primary_url = f"{self.base_url}/{year}.{month}/{ymd}/{md}tv1VA0_fwzx_电视天气预报_{ymd}{primary_time}.mp4"
        urls.append(primary_url)
        
        # 备用URL
        for t in self.fallback_times:
            if t != primary_time:  # 避免重复
                url = f"{self.base_url}/{year}.{month}/{ymd}/{md}tv1VA0_fwzx_电视天气预报_{ymd}{t}.mp4"
                urls.append(url)
        
        return urls, ymd, primary_time
    
    def download_video(self, url, save_path):
        """下载视频文件"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.zjqzqx.com/'
        }
        
        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            else:
                logging.warning(f"URL返回状态码: {response.status_code}")
                return False
        except Exception as e:
            logging.error(f"下载失败: {e}")
            return False
    
    def run(self):
        """主运行函数"""
        logging.info("开始执行天气预报视频下载任务")
        
        # 生成所有可能的URL
        urls, ymd, primary_time = self.generate_video_urls()
        save_path = f"weather_{ymd}.mp4"
        
        # 检查文件是否已存在
        if os.path.exists(save_path):
            logging.info(f"视频文件已存在: {save_path}")
            return True
        
        logging.info(f"生成 {len(urls)} 个候选URL，首选时间戳: {primary_time}")
        
        # 尝试所有URL
        for i, url in enumerate(urls):
            logging.info(f"尝试第 {i+1} 个URL: {url}")
            
            if self.download_video(url, save_path):
                # 提取成功的时间戳
                success_time = url[-14:-4]  # 提取时间戳部分
                self.update_success_log(success_time)
                logging.info(f"视频下载成功: {save_path}")
                return True
            
            # 添加延迟避免请求过快
            time.sleep(2)
        
        # 所有URL都失败
        logging.error("所有URL尝试均失败")
        return False

def main():
    downloader = WeatherVideoDownloader()
    success = downloader.run()
    
    if not success:
        # 这里可以添加通知功能，如发送邮件或短信
        logging.error("视频下载失败，需要手动处理")
    
    logging.info("任务执行完毕")

if __name__ == "__main__":
    main()