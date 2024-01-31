import scrapy
from urllib.parse import urlparse
from scrapy_splash import SplashRequest
import csv

class ImdbSpider(scrapy.Spider):
    # название spider
    name = 'imdb'
    # URL-адрес главной страницы с жанрами
    start_urls = ['https://www.imdb.com/feature/genre/?ref_=nv_ch_gr']

    def parse(self, response):
        # Извлечение ссылок на страницы с жанрами
        genre_links = response.css('div.ipc-chip-list--base a::attr(href)').getall()
        for link in genre_links:
            # Проверяем, имеет ли ссылка схему
            if urlparse(link).scheme == '':
                link = response.urljoin(link)
            # Отправляем запрос на страницу жанра
            yield scrapy.Request(url=link, callback=self.parse_movie_details)

    def parse_movie_details(self, response):
        title = response.css('h1.ipc-page-title__title::text').get()
        year = response.css('.ipc-inline-list__item:nth-child(1)::text').get()
        # Извлекаем рейтинг
        rating = response.xpath('//span[contains(@class, "ipc-rating-star--imdb-rating")]/text()').get()

        director = response.css('.sc-a78ec4e3-2.gmHPTF a::text').get()

        # Жанры фильма
        genres = response.css('[data-testid="btp_gl"] li::text').getall()

        # Запись данных в CSV-файл
        with open('imdb_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Year', 'Rating', 'Director', 'Genres']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Проверка наличия заголовоков в файле
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'Title': title, 'Year': year, 'Rating': rating, 'Director': director, 'Genres': genres})