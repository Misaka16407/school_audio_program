import requests
#状态分析：视频地址为动态生成
#
#
# 设置浏览器UA和Referer（模拟正常访问）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Referer': 'https://www.zjqzqx.com/'
}

# 测试1
video_url = " "
response = requests.get(video_url, headers=headers)

# 检查响应状态和内容类型
print(f"状态码: {response.status_code}")
print(f"内容类型: {response.headers.get('Content-Type')}")
print(f"前100字节: {response.content[:100]}")  # 如果是MP4文件会显示二进制乱码

page_url = "https://www.zjqzqx.com/wechat/television.html"
page_response = requests.get(page_url, headers=headers)