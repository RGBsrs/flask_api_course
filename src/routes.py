from src.resources.aggregations import AggregationApi
from src import app
from src.resources.actors import ActorListApi
from src.resources.films import FilmListApi
from src.resources.aggregations import AggregationApi 




film_list_api = FilmListApi.as_view('films')
app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)

actor_list_api = ActorListApi.as_view('actors')
app.add_url_rule('/actors', view_func=actor_list_api , strict_slashes = False)
app.add_url_rule('/actors/<name>', view_func=actor_list_api, strict_slashes = False)

aggregation_api = AggregationApi.as_view('aggregation')
app.add_url_rule('/aggregations', view_func=aggregation_api, strict_slashes = False)