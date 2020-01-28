
from app_main import app
from tests import OhmTestCase


class CommunityTest(OhmTestCase):
    def test_get(self):
        with app.test_client() as c:
            response = c.get('/community')
            assert "Welcome our newest users" in response.data
            assert "Justin Bieber" in response.data
