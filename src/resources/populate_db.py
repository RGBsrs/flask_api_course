import datetime
from threading import Thread
from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor
#from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor

import requests
import bs4

from flask.views import MethodView

from src import db
from src.services.film_service import FilmService


def convert_time(time: str):
    hour, minute = time.split('h')
    minutes = (int(hour) * 60) + int(minute.strip('min'))
    return minutes


class PopulateDB(MethodView):
    url = 'https://www.imdb.com/'        

    def post(self):
        t0 = datetime.datetime.now()
        films_urls = self.get_films_urls()
        films = self.parse_films(films_urls)
        created_films = self.populate_db_with_films(films)
        dt = datetime.datetime.now() - t0
        print(f'Populating time :{dt.total_seconds():.2f} sec.')
        return {'Message' : f'Database populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting film urls', flush=True)
        url = self.url + 'chart/top'
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('td', class_ = 'posterColumn')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:10]
        return movie_links

    def parse_films(self, film_urls):
        films_to_create = []
        for url in film_urls:
            url = self.url + url
            print(f'Get detailed info about film: {url}')
            film_content = requests.get(url)
            film_content.raise_for_status()
            html = film_content.text
            soup = bs4.BeautifulSoup(html, features='html.parser')
            title,_ = soup.find('div', class_ = 'originalTitle').text.split('(')
            rating = float(soup.find('div', class_ = 'ratingValue').strong.text)
            description = soup.find('div', class_ = 'summary_text').text.strip()
            title_bar = soup.find('div', class_ = 'titleBar').text.strip()
            title_content = title_bar.split('\n')
            release_date, _ = title_content[-1].split('(')
            release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
            length = convert_time(soup.find('div', class_ = 'subtext').time.text.strip())
            print(f'Recived info about: {title}', flush = True)
            films_to_create.append(
                {
                    'title' : title,
                    'rating' : rating,
                    'description' : description,
                    'release_date' : release_date,
                    'length' : length,
                    'distributed_by' : 'Warner Bros. Pictures',
                }
            )
        return films_to_create

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)

class PopulateDBThreaded(MethodView):   
    url = 'https://www.imdb.com/'        

    def post(self):
        threads = []
        films_to_create = []
        t0 = datetime.datetime.now()
        films_urls = self.get_films_urls()
        for film_url in films_urls:
            threads.append(Thread(target=self.parse_film,args=(film_url, films_to_create), daemon=True))
        [t.start() for t in threads]
        [t.join() for t in threads]                        

        created_films = self.populate_db_with_films(films_to_create)
        dt = datetime.datetime.now() - t0
        print(f'Populating time :{dt.total_seconds():.2f} sec.')

        return {'Message' : f'Database populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting film urls', flush=True)
        url = self.url + 'chart/top'
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('td', class_ = 'posterColumn')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:11]
        return movie_links

    def parse_film(self, url, films_to_create):
        url = self.url + url
        print(f'Get detailed info about film: {url}')
        film_content = requests.get(url)
        film_content.raise_for_status()
        html = film_content.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        title,_ = soup.find('div', class_ = 'originalTitle').text.split('(')
        rating = float(soup.find('div', class_ = 'ratingValue').strong.text)
        description = soup.find('div', class_ = 'summary_text').text.strip()
        title_bar = soup.find('div', class_ = 'titleBar').text.strip()
        title_content = title_bar.split('\n')
        release_date, _ = title_content[-1].split('(')
        release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
        length = convert_time(soup.find('div', class_ = 'subtext').time.text.strip())
        print(f'Recived info about: {title}', flush = True)
        films_to_create.append(
            {
                'title' : title,
                'rating' : rating,
                'description' : description,
                'release_date' : release_date,
                'length' : length,
                'distributed_by' : 'Warner Bros. Pictures',
            }
        )

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)

class PopulateDBThreadPoolExecutor(MethodView):
    url = 'https://www.imdb.com/'        

    def post(self):
        t0 = datetime.datetime.now()
        film_urls = self.get_films_urls()
        work = []
        with PoolExecutor() as executor:
            for film_url in film_urls:
                f = executor.submit(self.parse_film, film_url)
                work.append(f)
        films_to_create = [f.result() for f in work]
        created_films = self.populate_db_with_films(films_to_create)
        dt = datetime.datetime.now() - t0
        print(f'Populating time :{dt.total_seconds():.2f} sec.')

        return {'Message' : f'Database populated with {created_films} films'}, 201

    def get_films_urls(self):
        print('Getting film urls', flush=True)
        url = self.url + 'chart/top'
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        movie_containers = soup.find_all('td', class_ = 'posterColumn')
        movie_links = [movie.a.attrs['href'] for movie in movie_containers][:11]
        return movie_links

    def parse_film(self, url):
        url = self.url + url
        print(f'Get detailed info about film: {url}')
        film_content = requests.get(url)
        film_content.raise_for_status()
        html = film_content.text
        soup = bs4.BeautifulSoup(html, features='html.parser')
        title,_ = soup.find('div', class_ = 'originalTitle').text.split('(')
        rating = float(soup.find('div', class_ = 'ratingValue').strong.text)
        description = soup.find('div', class_ = 'summary_text').text.strip()
        title_bar = soup.find('div', class_ = 'titleBar').text.strip()
        title_content = title_bar.split('\n')
        release_date, _ = title_content[-1].split('(')
        release_date = datetime.datetime.strptime(release_date.strip(), '%d %B %Y')
        length = convert_time(soup.find('div', class_ = 'subtext').time.text.strip())
        print(f'Recived info about: {title}', flush = True)
        return {
                'title' : title,
                'rating' : rating,
                'description' : description,
                'release_date' : release_date,
                'length' : length,
                'distributed_by' : 'Warner Bros. Pictures',
                }

    @staticmethod
    def populate_db_with_films(films):
        return FilmService.bulk_create_films(db.session, films)