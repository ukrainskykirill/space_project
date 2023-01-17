from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .services.nasa_photo import get_nasa_picture
from .services.asteroids import get_asteroids
from .services.nasa_photo_by_days import get_previous_photo
from space.settings import logger
from .utils import menu


async def picture_of_the_day(request: HttpRequest) -> HttpResponse:
    logger.info('View  - get picture of the day')
    photo, text, previous = await get_nasa_picture()
    context = {'context': text, 'photo': photo, 'previous': previous, 'menu': menu}
    return render(request, template_name='nasa_api/picture_of_the_day.html', context=context)


async def pictures_by_days(request: HttpRequest, id: int) -> HttpResponse:
    logger.info('View  - get previous pictures of the day')
    photo, text, previous, next = await get_previous_photo(id)
    context = {'context': text, 'photo': photo, 'previous': previous, 'next': next, 'menu': menu}
    return render(request, template_name='nasa_api/picture_of_the_day.html', context=context)


async def dengerous_asteroids(request: HttpRequest) -> HttpResponse:
    logger.info('View  - get asteroids')
    asteroids = await get_asteroids()
    context = {'asteroids': asteroids, 'menu': menu}
    return render(request, template_name='nasa_api/asteroids.html', context=context)


async def error_400(request, exception):
    return render(request, template_name='nasa_api/400.html', status=400)


async def error_404(request, exception):
    return render(request, template_name='nasa_api/404.html', status=404)
