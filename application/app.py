from sanic import Sanic

from .database.db import database_connection, setup_database
from .routes import api

DB_NAME = "database.db"


async def setup_db(app):
    app.ctx.db = await database_connection(DB_NAME)
    await setup_database(app.ctx.db)


def create_app():
    try:
        app = Sanic("webapp")
        app.blueprint(api)

        app.register_listener(setup_db, "before_server_start")

        return app
    except Exception as e:
        print(e)
        exit
