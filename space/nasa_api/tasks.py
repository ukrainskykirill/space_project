import datetime

from redis.exceptions import ConnectionError
import requests
from celery import Task

from space.settings import MEDIA_URL, MEDIA_ROOT, URL_NASA_ASTEROIDS
from nasa_api.models import Photo, Asteroids
from space.celery import app
from space.redis import sync_redis
from space.settings import URL_NASA_PIC_OF_THE_DAY, NASA_API_KEY, logger
from nasa_api.schemas import AsteroidsData

day1 = str(datetime.date.today())
day2 = str(datetime.date.today() - datetime.timedelta(days=1))


class PhotoOfTheDay(Task):
    ignore_result = True
    name = 'get_photo'

    def __init__(self):
        self.params = {
            'api_key': NASA_API_KEY
        }

    def save_photo(self, url: str) -> str:
        try:
            get_photo = requests.get(url)
            file = f'nasa_picture/{datetime.date.today()}.jpg'
            out = open(f'{MEDIA_ROOT}/{file}', "wb")
            out.write(get_photo.content)
            out.close()
            photo = f'{MEDIA_URL}{file}'
            return photo
        except requests.exceptions.RequestException:
            logger.warning("There's not connection with API")

    def db_save(self, text: str, file: str) -> None:
        try:
            data_base = Photo(
                text=text,
                file=file,
            )
            data_base.save()
        except Exception:
            logger.warning("Problem with DB in task")

    def save_cache(self, text: str, file: str) -> None:
        day = str(datetime.date.today())
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        try:
            sync_redis.delete(yesterday)
            sync_redis.lpush(day, text)
            sync_redis.lpush(day, file)
        except ConnectionError:
            logger.warning('No connection with Redis')

    def get_data(self, url: str, params: dict) -> None:
        try:
            result = requests.get(url=url, params=params)
            text = result.json().get('explanation')
            file = self.save_photo(url=result.json().get('url'))
            self.db_save(text=text, file=file)
            self.save_cache(text=text, file=file)
        except requests.exceptions.RequestException:
            logger.warning("There's not connection with API")

    def run(self, source: any, *args, **kwargs) -> None:
        logger.info("Start to do task")
        self.source = source
        self.get_data(url=URL_NASA_PIC_OF_THE_DAY, params=self.params)


class Asteroid(Task):
    name = 'get_asteroids'

    def __init__(self):
        self.params = {
            'start_date': day2,
            'end_date': day1,
            'api_key': NASA_API_KEY
        }

    def save_db(self, asteroids: AsteroidsData) -> None:
        try:
            for asteroid in asteroids.near_earth_objects.day:
                if not asteroid.is_potentially_hazardous_asteroid:
                    db = Asteroids(
                        name=asteroid.name,
                        nasa_jpl_url=asteroid.nasa_jpl_url,
                        estimated_diameter_min=asteroid.estimated_diameter.kilometers.get('estimated_diameter_min'),
                        estimated_diameter_max=asteroid.estimated_diameter.kilometers.get('estimated_diameter_max'),
                        close_approach_data=asteroid.close_approach_data[0].get('close_approach_date_full')
                    )
                    db.save()
        except Exception:
            logger.warning("Problem with DB in task")

    def get_data(self) -> None:
        try:
            res = requests.get(url=URL_NASA_ASTEROIDS, params=self.params)
            asteroids = AsteroidsData.parse_obj(res.json())
            self.save_db(asteroids)
        except requests.exceptions.RequestException:
            logger.warning("There's not connection with API")

    def run(self, source: any, *args, **kwargs) -> None:
        logger.info("Start to do task")
        self.source = source
        self.get_data()


app.register_task(PhotoOfTheDay())
app.register_task(Asteroid())
