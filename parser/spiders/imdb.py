import scrapy
from urllib.parse import urlparse
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
        movies = response.css('li.ipc-metadata-list-summary-item')

        with open('imdb_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'year', 'imdb_rating', 'genre']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for movie in movies:
                title = movie.css('.ipc-title__text::text').get()
                year = movie.css('.dli-title-metadata-item:nth-child(1)::text').get()
                imdb_rating = movie.css('.ipc-rating-star.ipc-rating-star--base.ipc-rating-star--imdb.ratingGroup--imdb-rating::text').get()
                genre = movie.css('.dli-title-type-data::text').get()

                writer.writerow({
                    'title': title,
                    'year': year,
                    'imdb_rating': imdb_rating,
                    'genre': genre
                })

