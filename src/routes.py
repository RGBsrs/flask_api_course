from src import app
from src.resources.actors import ActorListApi
from src.resources.films import FilmListApi




film_list_api = FilmListApi.as_view('films')
app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)

actor_list_api = ActorListApi.as_view('actors')
app.add_url_rule('/actors', view_func=actor_list_api , strict_slashes = False)
app.add_url_rule('/actors/<name>', view_func=actor_list_api, strict_slashes = False)