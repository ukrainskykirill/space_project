import datetime

from nasa_api.models import Asteroids
from space.settings import logger


async def get_asteroids() -> list:
    daily_asteroids = []
    five_asteroid = []
    today = str(datetime.date.today())
    async for asteroid in Asteroids.objects.filter(date=today):
        daily_asteroids.append(asteroid)
    if len(daily_asteroids) < 5:
        logger.info('get last 5 asteroids')
        async for asteroid in Asteroids.objects.order_by('-id')[:5]:
            five_asteroid.append(asteroid)
        return five_asteroid
    logger.info('get daily asteroids')
    return daily_asteroids
