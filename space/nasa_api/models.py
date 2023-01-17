from django.db import models


class Photo(models.Model):
    text = models.CharField(max_length=3000)
    date = models.DateField(auto_now=True)
    file = models.ImageField(upload_to='nasa_pic_of_the_day')

    def get_absolute_url(self):
        return f'{self.id}'


class Asteroids(models.Model):
    name = models.CharField(max_length=200)
    nasa_jpl_url = models.CharField(max_length=500)
    estimated_diameter_min = models.FloatField()
    estimated_diameter_max = models.FloatField()
    close_approach_data = models.CharField(max_length=50)
    date = models.DateField(auto_now=True)
