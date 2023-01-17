import datetime

from redis.exceptions import ConnectionError
from django.http import Http404

from space.redis import async_redis
from nasa_api.models import Photo
from space.settings import logger


async def get_previous_day(day: str) -> any:
    try:
        photo = await Photo.objects.aget(date=day)
        previous = await Photo.objects.aget(pk=photo.pk-1)
    except Photo.DoesNotExist:
        logger.info("There'is previous photo")
        previous = None
    return previous


async def get_nasa_picture() -> any:
    day = str(datetime.date.today())
    try:
        data_list = await async_redis.lrange(day, 0, 1)
        if data_list:
            logger.info("Get_photo_from_cache")
            previous = await get_previous_day(day)
            photo = data_list[0]
            text = data_list[1]
            return photo, text, previous
    except ConnectionError:
        logger.warning("No connection with Redis")
        pass
    try:
        photo = await Photo.objects.aget(date=day)
        previous = await get_previous_day(day)
    except Photo.DoesNotExist:
        logger.info("There's not today photo")
        raise Http404
    return photo.file, photo.text, previous
