import pytest
from app import PeppyApp


@pytest.fixture
def app():
    return PeppyApp()


@pytest.fixture
def test_client(app):
    return app.test_session()
