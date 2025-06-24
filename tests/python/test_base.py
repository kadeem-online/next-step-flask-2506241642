# Main application test file

def test_app_initialization(app):
    """
    Test that the app initializes correctly.
    """

    assert app is not None
    assert app.config["TESTING"] is True
