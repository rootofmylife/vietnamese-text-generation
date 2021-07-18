import scrapy


class VozSpider(scrapy.Spider):
    name = 'voz'
    start_urls = ['https://voz.vn/f/chuyen-tro-linh-tinh.17/']
    custom_settings = { 'FEED_URI': "voz_%(time)s.json",
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        print("Current URL: {}".format(response.url))

        if "https://voz.vn/f/chuyen-tro-linh-tinh.17/page-3" in response.url:
            return

        post_urls = response.xpath('//div[@class="structItem-title"]//a/@href').extract()
        for url_item in post_urls:
            yield scrapy.Request('https://voz.vn' + url_item, callback=self.content_parse)

        next_page = response.xpath('//a[contains(@class, "pageNav-jump--next")]//@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def content_parse(self, response):
        yield {
                'url': response.url,
                'title': response.xpath('//h1[contains(@class, "p-title-value")]/text()').get().strip(),
                'text': ' '.join(response.xpath('//div[contains(@class, "bbWrapper")]//text()').extract()).strip(),
            }

        next_page = response.xpath('//a[contains(@class, "pageNav-jump--next")]//@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.content_parse)
