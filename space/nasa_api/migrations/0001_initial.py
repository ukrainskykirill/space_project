# Generated by Django 4.1.4 on 2023-01-17 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asteroids",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("nasa_jpl_url", models.CharField(max_length=500)),
                ("estimated_diameter_min", models.FloatField()),
                ("estimated_diameter_max", models.FloatField()),
                ("close_approach_data", models.CharField(max_length=50)),
                ("date", models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=3000)),
                ("date", models.DateField(auto_now=True)),
                ("file", models.ImageField(upload_to="nasa_pic_of_the_day")),
            ],
        ),
    ]
