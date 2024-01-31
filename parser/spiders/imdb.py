import scrapy
from urllib.parse import urlparse
import csv

# class ImdbSpider(scrapy.Spider):
#     # название spider
#     name = 'imdb'
#     # URL-адрес главной страницы с жанрами
#     start_urls = ['https://www.imdb.com/feature/genre/?ref_=nv_ch_gr']
#
#     def parse(self, response):
#         # Извлечение ссылок на страницы с жанрами
#         genre_links = response.css('div.ipc-chip-list--base a::attr(href)').getall()
#         for link in genre_links:
#             yield scrapy.Request(url=link, callback=self.parse_genre)
#
#     def parse_genre(self, response):
#         # Извлечение ссылок на страницы с фильмами внутри жанра
#         movie_links = response.css('li.ipc-metadata-list-summary-item a::attr(href)').getall()
#         for link in movie_links:
#             yield scrapy.Request(url=link, callback=self.parse_movie)
#
#
#
#     def parse_movie(self, response):
#         # Извлечение данных о фильме (название, год, рейтинг)
#         title = response.css('h3.ipc-title__text::text').get()
#         year = response.css('span.dli-title-metadata-item::text').get()
#         rating = response.css('span.aria-label::text').get()
#
#         # Извлечение ссылок на страницы с информацией о режиссерах
#         director_links = response.css('ul.directors-list a::attr(href)').getall()
#         for link in director_links:
#             yield scrapy.Request(url=link, callback=self.parse_director)
#
#         yield {
#             'Title': title,
#             'Year': year,
#             'Rating': rating
#         }
#
#     def parse_director(self, response):
#         # Извлечение информации о режиссере
#         director_name = response.css('a.ipc-metadata-list-item__list-content-item--link::before').get()
#         yield {
#             'Director': director_name
#         }



# class ImdbSpider(scrapy.Spider):
#     # название spider
#     name = 'imdb'
#     # URL-адрес главной страницы с жанрами
#     start_urls = ['https://www.imdb.com/feature/genre/?ref_=nv_ch_gr']
#
#     def parse(self, response):
#         # Извлечение ссылок на страницы с жанрами
#         genre_links = response.css('div.ipc-chip-list--base a::attr(href)').getall()
#         for link in genre_links:
#             # Проверяем, имеет ли ссылка схему
#             if urlparse(link).scheme == '':
#                 link = response.urljoin(link)
#             print(link)
#             yield scrapy.Request(url=link, callback=self.parse_genre)
#
#     def parse_genre(self, response):
#         # Извлечение ссылок на страницы с фильмами внутри жанра
#         movie_links = response.css('li.ipc-metadata-list-summary-item a::attr(href)').getall()
#         for link in movie_links:
#             # Проверяем, имеет ли ссылка схему
#             if urlparse(link).scheme == '':
#                 link = response.urljoin(link)
#
#             print(link)
#             yield scrapy.Request(url=link, callback=self.parse_movie)
#
#     def parse_movie(self, response):
#         # # Извлечение данных о фильме (название, год, рейтинг)
#         # title = response.css('h3.ipc-title__text::text').get(default='')
#         # year = response.css('span.dli-title-metadata-item::text').get(default='')
#         # rating = response.css('span.aria-label::text').get(default='')
#
#         # Извлечение ссылок на страницы с информацией о режиссерах
#         director_links = response.css('ul.directors-list a::attr(href)').getall()
#         for link in director_links:
#             # Проверяем, имеет ли ссылка схему
#             if urlparse(link).scheme == '':
#                 link = response.urljoin(link)
#
#             print(link)
#             yield scrapy.Request(url=link, callback=self.parse_director)
#         #
#         # yield {
#         #     'Title': title,
#         #     'Year': year,
#         #     'Rating': rating
#         # }
#
#     def parse_director(self, response):
#         # Извлечение данных о фильме (название, год, рейтинг)
#         title = response.css('span.hero__primary-text::text').get()
#         year = response.css('ul.ipc-inline-list li:nth-child(1) a::text').get()
#         rating = response.css('div[data-testid="hero-rating-bar__aggregate-rating__score"] span::text').get()
#
#         # Извлечение имени режиссера и страны производства
#         director = response.css('div.sc-69e49b85-0.jqlHBQ a[href*="/name/"] span::text').get()
#         country = response.css('div.sc-69e49b85-0.jqlHBQ a[href*="/search/title?country_of_origin="]::text').get()
#
#         yield {
#             'Title': title,
#             'Year': year,
#             'Rating': rating,
#             'Director': director,
#             'Country': country
#         }
#
#         # Запись данных в CSV-файл
#         with open('imdb_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
#             fieldnames = ['Title', 'Year', 'Rating', 'Director', 'Country']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#
#             # Проверка наличия заголовоков в файле
#             if csvfile.tell() == 0:
#                 writer.writeheader()
#
#             writer.writerow({'Title': title, 'Year': year, 'Rating': rating, 'Director': director, 'Country': country})



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
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_genre)

    def parse_genre(self, response):
        # Извлечение ссылок на страницы с фильмами внутри жанра
        movie_links = response.css('li.ipc-metadata-list-summary-item a::attr(href)').getall()
        for link in movie_links:
            # Проверяем, имеет ли ссылка схему
            if urlparse(link).scheme == '':
                link = response.urljoin(link)

            print(link)
            yield scrapy.Request(url=link, callback=self.parse_movie)

    def parse_movie(self, response):
        # Извлечение данных о фильме (название, год, рейтинг)
        title = response.css('span.hero__primary-text::text').get()
        year = response.css('li.ipc-inline-list__item::text').extract_first()
        rating = response.css('div[data-testid="hero-rating-bar__aggregate-rating__score"] span::text').get()

        # Извлечение имени режиссера и страны производства
        director = response.css('div.ipc-metadata-list-item__content-container::text').get()
        country = response.css('div.sc-69e49b85-0.jqlHBQ a[href*="/search/title?country_of_origin="]::text').get()

        # Запись данных в CSV-файл
        with open('imdb_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Year', 'Rating', 'Director', 'Country']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Проверка наличия заголовоков в файле
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'Title': title, 'Year': year, 'Rating': rating, 'Director': director, 'Country': country})
