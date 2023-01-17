# SPACE PROJECT 🛰

<b><em>It's async Django pet project which use NASA API to create two endpoints:</b></em>

1. GET <b><em>nasa_api/pic</em></b>  - to check NASA photo of the day with some description. Also you can check previous photos.
2. GET <b><em>nasa_api/asteroid</em></b> - to check daily dangerous asteroids for the Earth.

<b>STACK</b>:
1. <b>Django async</b> - there's async code in full Django project.
2. <b>Celery + Redis</b> - I use Celery to get data from NASA API once a day and I cache some discription to make daily photo endpoint more fast.
