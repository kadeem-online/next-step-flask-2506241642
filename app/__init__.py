# standard library imports
import json
import logging

# third party imports
from dotenv import load_dotenv
from flask import (Flask, render_template, url_for)

# local imports
import app.extensions as Extensions
from app.utilities.functions import (is_development)


# configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def create_app(is_test=False, custom_config=None):
    """
    Generates the main application instance.

    Args:
        is_test (bool): Flag to indicate if the application is in test mode.
        custom_config (dict): Custom configuration settings for the application.
            These settings will override the default configuration.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Load manifest from vite
    manifest_path = 'app/static/dist/.vite/manifest.json'
    if not is_development():
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
        except FileNotFoundError:
            print(f'Error: Could not load manifest file at {manifest_path}. ')
            print(f"{FileNotFoundError}")

    # set vite development URL
    vite_dev_url = 'http://localhost:5173'

    # Create flask application instance
    app = Flask(__name__, instance_relative_config=True)

    # log application startup
    app.logger.info('Starting application...')

    # Load the default configuration
    app.config.from_object('app.config.AppConfiguration')

    # Load mode specific configuration
    if is_test:
        app.config.from_object('app.config.TestingConfiguration')
    elif is_development():
        app.config.from_object('app.config.DevelopmentConfiguration')
    else:
        app.config.from_object('app.config.ProductionConfiguration')

    # Load custom configurations if provided
    try:
        if custom_config:
            app.config.update(custom_config)
    except Exception as e:
        app.logger.error(f"Error loading custom configuration: {e}")
        raise e

    # initialize extensions
    Extensions.db.init_app(app)
    Extensions.migrate.init_app(app, Extensions.db)

    # create vite asset helper
    def vite_asset(filename):
        """
        Returns the path to the asset file based on the environment.
        """
        if is_development():
            return f"{vite_dev_url}/{filename}"

        if manifest is None:
            app.logger.error(
                'Manifest file not found. Ensure the application is built with Vite.'
            )
            return "missing_resource"

        if manifest.get(f"{filename}") is None:
            app.logger.warning(
                f"Manifest file does not contain the expected '{filename}' key!"
            )
            return "missing_resource"

        file = manifest[f'{filename}'].get('file')
        if file is None:
            app.logger.error(
                f"File '{filename}' not found in manifest. Ensure the application is built with Vite."
            )
            return "missing_resource"

        return url_for('static', filename=f"dist/{file}")

    # set jinja2 global variables
    app.jinja_env.globals['is_development'] = is_development
    app.jinja_env.globals['vite_asset'] = vite_asset
    app.jinja_env.globals['vite_dev_url'] = vite_dev_url

    # Application route: index
    @app.route('/', strict_slashes=False)
    def index():
        """
        Index route.
        """
        return render_template('index.jinja2')

    # return the application instance
    app.logger.info('Application instance running...')
    return app


# Run the application if the file is executed directly
if __name__ == '__main__':
    app = create_app()
    app.run()
