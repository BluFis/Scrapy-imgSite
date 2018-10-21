# -*- coding: utf-8 -*-
import scrapy
# 导入item中结构化数据模板
from img.items import ImgItem
import time


class XhSpider(scrapy.Spider):
    # 爬虫名称，唯一
    name = "xh"
    # 允许访问的域
    allowed_domains = ["52zfl.vip"]
    # 初始URL
    start_urls = ['https://52zfl.vip/luyilu/list_5_1.html']

    def parse(self, response):
        items = []
        # 如果图片地址以http://www.xiaohuar.com/list-开头，我才取其名字及地址信息
        if response.url.startswith("https://52zfl.vip/luyilu/list_5_"):
            allPics = response.xpath('//article[@class="excerpt excerpt-one"]')
            for pic in allPics:
                # 分别处理每个图片，取出名称及地址
                item = ImgItem()
                name = pic.xpath('./header/h2/a/text()').extract()[0]
                addr = pic.xpath('./header/h2/a/@href').extract()[0]
                item['list_url'] = response.url
                item['page_url'] = 'https://52zfl.vip'+addr
                item['name'] = name
                count = self.findpage(name)
                items.append(item)
                for page_item in items:
                    index = 1;
                    while count > 0:
                        if index == 1:
                            next_url = page_item['page_url']
                        else:
                            b = page_item['page_url']
                            next_url = b[:b.find('.html')]+"_%s.html" % index
                        count -= 4
                        index += 1
                        yield scrapy.Request(url=next_url, meta={'item_1': page_item},
                                             callback=self.parse_page)

                for i in range(1, 92):
                    all_pages = 'https://52zfl.vip/luyilu/list_5_%s.html' % i
                    yield scrapy.Request(url=all_pages, callback=self.parse)

    def parse_page(self, response):
        items = response.meta['item_1']
        infos = response.xpath('//article[@class="article-content"]/p/img')
        print(len(infos))
        current_milli_time = lambda: int(round(time.time() * 1000))
        for info in infos:
            item = ImgItem()
            images_urls = info.xpath('@src')[0].extract()
            item['pic_url'] = images_urls
            item['name'] = items['name']
            item['pic_name'] = str(current_milli_time())
            item['list_url'] = items['list_url']
            item['page_url'] = items['page_url']
            print(item)
            yield item

    def findpage(self,name):
        co = name[name.find('[') + 1:name.find(']') - 1]
        if co.isdigit():
            return int(co)
        else:
            return self.findpage(name[name.find(']')+1:])



