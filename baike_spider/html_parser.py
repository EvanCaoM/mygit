
from bs4 import BeautifulSoup
import re
from urllib import parse

class HtmlParser(object):


    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # https://baike.baidu.com/item/%E6%B8%85%E5%8D%8E%E5%A4%A7%E5%AD%A6
        links = soup.find_all('a', href=re.compile(r"/item/"))
        for link in links:
            new_url = link["href"]
            new_full_url = parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        # <dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        # <dd class="lemmaWgt-lemmaTitle-title"><h1>Python技术手册</h1>
        res_data['url'] = page_url
        title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title'] = title_node.get_text()
        # <div class="para" label-module="para">《Python技术手册(第2版)》列举了<a target="_blank" href="/item/Python">Python</a>对象和模块中提供的所有类型、方法和函数，并辅以适当的示例，系统地展示了Python包含的功能及其使用方法<sup class="sup--normal" data-sup="1">
        # [1]</sup><a class="sup-anchor" name="ref_[1]_3981420">&nbsp;</a>。</div>
        summary_node = soup.find('div', class_ = "lemma-summary")
        res_data['summary'] = summary_node.get_text()
        return res_data


    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data