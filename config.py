import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """
    Configuration class for setting up the application's settings.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The database URI used by SQLAlchemy. 
            This value is loaded from the environment variable 'DATABASE_URL', 
            with a default fallback to 'postgresql://postgres:admin@localhost/postgres' if the environment variable is not set.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): A flag indicating whether SQLAlchemy should track modifications 
            of objects and emit signals. This is set to False to disable this feature and reduce overhead.

    This class is used to configure database connectivity and other settings for the application.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
