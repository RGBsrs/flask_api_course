import http
import json
from unittest.mock import patch

from src import app


class TestActors:
    name = []
    def test_get_actors_with_db(self):
        client = app.test_client()
        resp = client.get('/actors')

        assert resp.status_code == http.HTTPStatus.OK
    
    @patch('src.services.actor_service.ActorService.fetch_all_actors',
            autospec= True)
    def test_get_actors_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/actors')

        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_actor_with_db(self):
        client = app.test_client()
        data = {
            'name' : 'test',
            'birthday' : '2021-01-01',
            'is_active' : 'True'
        }
        resp = client.post('/actors', data = json.dumps(data), content_type = 'application/json')
        
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['name'] == 'test'
        self.name.append(resp.json['name'])

    def test_create_actor_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
            patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
            'name' : 'test',
            'birthday' : '2021-01-01',
            'is_active' : 'True'
            }
            resp = client.post('/actors', data = json.dumps(data), content_type = 'application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.name[0]}'
        data = {
            'name' : 'test',
            'birthday' : '2021-02-02',
            'is_active' : 'True'
            }
        resp = client.put(url, data = json.dumps(data), content_type = 'application/json')
        
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['birthday'] == '2021-02-02'

    def test_update_actor_mock_db(self):
        with patch('src.services.actor_service.ActorService.fetch_actor_by_name',
                    autospec=True) as mocked_query,\
            patch('src.db.session.add', autospec=True) as mock_session_add, \
            patch('src.db.session.commit', autospec=True) as mock_session_commit:
            url = f'/actors/{self.name[0]}'
            client = app.test_client()
            data = {
            'name' : 'test',
            'birthday' : '2021-02-02',
            'is_active' : 'True'
            }
            resp = client.patch(url, data = json.dumps(data), content_type = 'application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_actor_with_db(self):
        client = app.test_client()
        url = f'/actors/{self.name[0]}'
        resp = client.delete(url)

        assert resp.status_code == http.HTTPStatus.NO_CONTENT