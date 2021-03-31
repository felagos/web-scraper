from scrapy.crawler import CrawlerProcess
from spider import SpiderNews
import requests
import re


def get_my_ip(url='http://www.cualesmiip.com/', proxies=None):
    try:
        r = requests.get(url=url, proxies=proxies)
    except Exception as e:
        print('Error haciendo la request', e)
        return None

    if r.status_code != 200:
        print("Status Code:", r.status_code)
        return None

    regex = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    my_ip = regex.findall(r.text)
    return my_ip[1] if my_ip else None


def get_proxies():
    return {
        "http": "http://125.99.191.107:80",
        "https": "https://177.75.3.2:80"
    }

if __name__ == "__main__":
    proxies = get_proxies()
    ip = get_my_ip(proxies=proxies)
    print(ip)
    #process = CrawlerProcess()
    #process.crawl(SpiderNews)
    #process.start()
