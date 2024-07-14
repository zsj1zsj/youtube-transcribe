import requests
import xml.etree.ElementTree as ET
import html
import podsearch
import random
import html
import re


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
    ]
    return random.choice(user_agents)

def clean_html(raw_html):
    # 首先解码 HTML 实体
    decoded_html = html.unescape(raw_html)
    # 然后移除 HTML 标签
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', decoded_html)
    # 移除多余的空白字符
    cleantext = ' '.join(cleantext.split())
    return cleantext

def parse_lizhi_rss(url):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    # 获取RSS feed内容
    response = requests.get(url,headers=headers, timeout=10)
    
    if response.status_code != 200:
        print(f"Failed to fetch RSS feed. Status code: {response.status_code}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 characters of response
        return
    
    # 打印响应内容的前500个字符，以便检查
    # print(f"Response content (first 500 chars): {response.text[:500]}...")
    
    # 解析XML
    try:
        # 尝试解析XML
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"Failed to parse XML: {e}")
        return
    
    # 查找所有的<item>元素
    channel = root.find('channel')
    items = channel.findall('item')
    
    # 遍历并打印每个item的信息
    for item in items[0:30]:
        title = item.find('title').text if item.find('title') is not None else "No title"
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else "No date"
        
        enclosure = item.find('enclosure')
        audio_link = enclosure.get('url') if enclosure is not None else "No audio link"
        
        # 解析description字段，处理可能的None值
        description_elem = item.find('description')
        if description_elem is not None and description_elem.text is not None:
            description = html.unescape(description_elem.text)
        else:
            description = "No description available"
        
        print(f"Title: {title}")
        print(f"Published: {pub_date}")
        print(f"Audio Link: {audio_link}")
        print(f"Description: {clean_html(description.strip())}")
        print("-" * 50)

def podcast_find(keyword,country='cn'):
    print(f'keyword: {keyword}')
    podcasts = podsearch.search(keyword, country=country, limit=10)
    if podcasts:
        podcast = podcasts[0]
        print(podcast)
        return podcast.feed
    else:
        print(f"No podcasts found for keyword: {keyword}")
        return None

if __name__ == "__main__":
    # 使用函数
    # rss_url = "http://rss.lizhi.fm/rss/21148582.xml"
    # rss_url = "https://justpodmedia.com/rss/middle-ground.xml"
    rss_url = podcast_find('蜜獾')
    print(rss_url)
    parse_lizhi_rss(rss_url)
    
