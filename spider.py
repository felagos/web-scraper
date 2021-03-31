import scrapy


class SpiderNews(scrapy.Spider):
    __output_file = "results.json"

    name = "spider12S"
    allowed_domains = ["biobiochile.cl"]
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": __output_file, "FEED_EXPORT_ENCODING": "utf-8", "DEPTH_LIMIT": 2}
    start_urls = [
        "https://www.biobiochile.cl/lista/busca-2020/categorias/nacional",
        "https://www.biobiochile.cl/lista/busca-2020/categorias/internacional",
        "https://www.biobiochile.cl/lista/busca-2020/categorias/economia",
        "https://www.biobiochile.cl/lista/busca-2020/categorias/tendencias"
    ]

    def __init__(self):
        open(self.__output_file, "w").close()

    def parse(self, response):
        notes = response.xpath("//div[@class='results-container']/div[@class='results']/article[@class='article article-horizontal article-with-square']/a/@href").getall()
        for note in notes:
            yield response.follow(note, callback=self.parse_note)

    def parse_note(self, response):
        title = response.xpath("//h1[@class='post-title']/text()").get().strip()
        author = response.xpath("//div[@class='author']/div/div/span[@class='autor']/b/a/text()").get().strip()

        yield {"title": title, "author": author}
