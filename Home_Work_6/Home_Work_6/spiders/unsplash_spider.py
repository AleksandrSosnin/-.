import scrapy
from Home_Work_6.items import HomeWork6Item

class UnsplashSpider(scrapy.Spider):
    name = "unsplash_spider"
    start_urls = ["https://unsplash.com/t/nature"]

    def parse(self, response):
        for photo in response.css("figure a::attr(href)").getall():
            yield response.follow(photo, callback=self.parse_image)

    def parse_image(self, response):
        item = HomeWork6Item()
        item['image_url'] = response.css("meta[property='og:image']::attr(content)").get()
        item['image_title'] = response.css("meta[property='og:title']::attr(content)").get()
        item['category'] = response.url.split("/")[4] if len(response.url.split("/")) > 4 else "unknown"
        yield item
