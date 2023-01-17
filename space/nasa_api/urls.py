from django.urls import path

from . import views

urlpatterns = [
    path('pic/<int:id>', views.pictures_by_days, name='pic_by_days'),
    path('pic/', views.picture_of_the_day, name='pic'),
    path('asteroid/', views.dengerous_asteroids, name='asteroid'),
]