from src import app
from src.resources.smoke import Smoke
from src.resources.actors import ActorListApi
from src.resources.films import FilmListApi
from src.resources.populate_db import PopulateDB, PopulateDBThreaded, PopulateDBThreadPoolExecutor
from src.resources.aggregations import AggregationApi
from src.resources.auth import AuthLogin, AuthRegister

smoke_api = Smoke.as_view('smoke')
app.add_url_rule('/smoke', view_func=smoke_api, strict_slashes = False)

film_list_api = FilmListApi.as_view('films')
app.add_url_rule('/films', view_func=film_list_api, strict_slashes = False)
app.add_url_rule('/films/<uuid>', view_func=film_list_api, strict_slashes = False)

populate_db = PopulateDB.as_view('populate')
app.add_url_rule('/populate_db', view_func=populate_db, strict_slashes = False)

populate_db_threaded = PopulateDBThreaded.as_view('popultae_with_threads')
app.add_url_rule('/populate_db_threaded', view_func=populate_db_threaded, strict_slashes = False)

populate_db_executor = PopulateDBThreadPoolExecutor.as_view('popultae_with_executor')
app.add_url_rule('/populate_db_executor', view_func=populate_db_executor, strict_slashes = False)

actor_list_api = ActorListApi.as_view('actors')
app.add_url_rule('/actors', view_func=actor_list_api , strict_slashes = False)
app.add_url_rule('/actors/<name>', view_func=actor_list_api, strict_slashes = False)

aggregation_api = AggregationApi.as_view('aggregation')
app.add_url_rule('/aggregations', view_func=aggregation_api, strict_slashes = False)

auth_register = AuthRegister.as_view('auth_register')
app.add_url_rule('/register',  view_func=auth_register, strict_slashes = False)

auth_login = AuthLogin.as_view('auth_login')
app.add_url_rule('/login',  view_func=auth_login, strict_slashes = False)