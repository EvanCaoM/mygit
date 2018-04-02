import requests
import threading
from bs4 import BeautifulSoup
from lxml import etree


def get_html(url):
    # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    request = requests.get(url=url,headers=headers)
    response = request.text
    return response

def get_img_html(html):
    soup = BeautifulSoup(html,'lxml')
    all_a = soup.find_all('a',class_='list-group-item')
    # https://ws1.sinaimg.cn/bmiddle/9150e4e5ly1fpqucfg4s6j20b40cigmb.jpg
    # all_a = soup.find_all('a', href=re.compile(r"https://ws1.sinaimg.cn//bmiddle/"))

    for link in all_a:
        img_html = get_html(link['href'])
        img_html+=img_html
        return img_html

def get_img(html):
    soup = etree.HTML(html)
    items = soup.xpath('//div[@class="artile_des"]')
    for item in items:
        imgurl_list=item.xpath('table/tbody/tr/td/a/img/@onerror')
        start_save_img(imgurl_list)

def save_img(img_url):
    img_url = img_url.split('=')[-1][1:-2].replace('jp','jpg')
    print(u'正在下载'+'http:'+img_url)
    img_content=requests.get('http:'+img_url).content
    with open('Z:\mygit\doutu_spider\%s.jpg' % img_url.split('/')[-1],'wb') as f:
        f.write(img_content)

def start_save_img(imgurl_list):
    for i in imgurl_list:
        th=threading.Thread(target=save_img,args=(i,))
        th.start()

def main():
    start_url='https://www.doutula.com/article/list/?page={}'
    for i in range(1,100):
        start_html=get_html(start_url.format(i))
        html=get_img_html(start_html)
        get_img(html)

main()
print("爬虫结束")