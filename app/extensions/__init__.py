# third party imports
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# create an instance of SQLAlchemy
db = SQLAlchemy()

# create an instance of Migrate
migrate = Migrate()
