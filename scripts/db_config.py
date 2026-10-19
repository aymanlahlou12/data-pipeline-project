import os

from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def create_mysql_engine():
    password = os.getenv("MYSQL_PASSWORD")
    if not password:
        raise RuntimeError("MYSQL_PASSWORD must be set in the environment.")

    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("MYSQL_USER", "weather_app"),
        password=password,
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        database=os.getenv("MYSQL_DATABASE", "weather_etl"),
    )
    return create_engine(url)
