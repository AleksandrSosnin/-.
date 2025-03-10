import scrapy

class BestBooksSpider(scrapy.Spider):
    name = "best_books"
    allowed_domains = ["www.goodreads.com"]
    start_urls = ["https://www.goodreads.com/list/show/1.Best_Books_Ever"]

    page_count = 0
    max_pages = 3  

    def parse(self, response):
        self.page_count += 1
        for book in response.css('tr[itemtype="http://schema.org/Book"]'):
            yield {
                'title': book.css('a.bookTitle span::text').get(),
                'author': book.css('a.authorName span::text').get(),
                'rating': book.css('span.minirating::text').get().strip(),
            }
        if self.page_count < self.max_pages:
            next_page = response.css('a.next_page::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse)
        else:
            self.logger.info(f"Парсинг завершен. Обработано {self.page_count} страниц.")