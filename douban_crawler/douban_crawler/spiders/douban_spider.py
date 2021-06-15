import scrapy
from items import DoubanCrawlerItem

class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名字
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口URL，进入调度器的第一个URL
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for item in movie_list:
            movie_item = DoubanCrawlerItem()

            movie_item['serial_number'] = item.xpath(".//div[@class='item']//em/text()").extract_first()

            movie_item['movie_name'] = item.xpath(".//div[@class='info']//div[@class='hd']//a//span[1]/text()").extract_first()

            for i_content in item.xpath(".//div[@class='info']//div[@class='bd']//p[1]/text()").extract():
                content_s = "".join(i_content.split())
                movie_item['introduce'] = content_s

            movie_item['star'] = item.xpath(".//span[@class='rating_num']/text()").extract_first()

            movie_item['evaluate'] = item.xpath(".//div[@class='star']//span[4]/text()").extract_first()

            movie_item['describe'] = item.xpath(".//p[@class='quote']/span/text()").extract_first()

            # 将数据yield到pipeline中
            yield movie_item

        # 解析下一页，取得页面内"后一页"对应的XPath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250" + next_link, callback=self.parse)


