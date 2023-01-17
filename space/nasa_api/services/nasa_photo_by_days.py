from django.http import Http404

from nasa_api.models import Photo
from space.settings import logger


async def get_days(id: int) -> any:
    try:
        next = await Photo.objects.aget(pk=id+1)
    except Photo.DoesNotExist:
        logger.info("There'is no next photo")
        next = None
    try:
        prev = await Photo.objects.aget(pk=id-1)
    except Photo.DoesNotExist:
        prev = None
        logger.info("There'is no previous photo")
    return prev, next


async def get_previous_photo(id: int) -> any:
    try:
        photo = await Photo.objects.aget(pk=id)
        previous_day, next_day = await get_days(id)
        return photo.file, photo.text, previous_day, next_day
    except Photo.DoesNotExist:
        logger.info(f"There'is no photo with this id - {id}")
        raise Http404
