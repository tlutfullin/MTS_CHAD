import scrapy
from urllib.parse import urlparse
import csv

class ImdbSpider(scrapy.Spider):
    # название spider
    name = 'imdb'
    # URL-адрес главной страницы с жанрами
    start_urls = ['https://www.imdb.com/feature/genre/?ref_=nv_ch_gr']


    # Открытие файла для записи заголовков
    with open('imdb_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'year', 'imdb_rating', 'genre']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Запись заголовков, если файл пуст
        if csvfile.tell() == 0:
            writer.writeheader()

    def parse(self, response):
        # Извлечение ссылок на страницы с жанрами
        genre_links = response.css('div.ipc-chip-list--base a::attr(href)').getall()
        genre_titles = response.css('.ipc-chip__text::text').getall()

        #print(genre_titles)

        for link, genre_title in zip(genre_links, genre_titles):
            # Проверяем, имеет ли ссылка схему
            if urlparse(link).scheme == '':
                link = response.urljoin(link)

            # Создание запроса на вторую страницу с передачей данных через метаданные
            yield scrapy.Request(url=link, callback=self.parse_movie_details,
                                 meta={'genre_title':genre_title})

    def parse_movie_details(self, response):

        # Извлечение переданных данных из метаданных
        passed_data = response.meta.get('genre_title')
        #print('Извлеченные данные',passed_data)

        movies = response.css('li.ipc-metadata-list-summary-item')

        with open('imdb_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'year', 'imdb_rating', 'genre']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


            for movie in movies:
                title = movie.css('.ipc-title__text::text').get()
                year = movie.css('.dli-title-metadata-item:nth-child(1)::text').get()
                imdb_rating = movie.css('.ipc-rating-star.ipc-rating-star--base.ipc-rating-star--imdb.ratingGroup--imdb-rating::text').get()
                #genre = movie.css('.dli-title-type-data::text').get()
                genre = passed_data

                writer.writerow({
                    'title': title,
                    'year': year,
                    'imdb_rating': imdb_rating,
                    'genre': genre
                })

