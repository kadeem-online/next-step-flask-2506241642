# standard libraries
import tempfile

#  third party libraries
import pytest

# local libraries
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """
    The main flask app fixture for the tests.
    """
    _, db_path = tempfile.mkstemp(suffix=".db")

    test_config = {
        "TESTING": True,

        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    app = create_app(is_test=True, custom_config=test_config)
    yield app


@pytest.fixture(scope="session")
def client(app):
    """
    The test client fixture for the app.
    """
    client = app.test_client()
    yield client


@pytest.fixture(scope="session")
def app_ctx(app):
    """
    Pass the app context as a fixture.
    """
    with app.app_context():
        yield


@pytest.fixture(scope="session")
def db(app, app_ctx):
    """
    The database fixture for tests.
    """
    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture(scope="function")
def session(app, db, app_ctx):
    """
    The session fixture for tests.
    """

    connection = db.engine.connect()
    transaction = connection.begin()

    session = db._make_scoped_session(bind=connection)
    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
