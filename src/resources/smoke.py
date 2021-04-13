from flask.views import MethodView


class Smoke(MethodView):
    def get(self):
        return {'message': 'OK'}