# Main application test file

def test_app_initialization(app):
    """
    Test that the app initializes correctly.
    """

    assert app is not None
    assert app.config["TESTING"] is True


def test_client_initialization(client):
    """
    Test that the client initializes correctly.
    """

    assert client is not None
    assert hasattr(client, "get")
    assert hasattr(client, "post")
    assert hasattr(client, "put")
    assert hasattr(client, "delete")


def test_home_page(client):
    """
    Test that the homepage loads correctly
    """

    response = client.get('/')

    assert response.status_code == 200
