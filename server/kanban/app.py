import os
from flask import Flask
from kanban.db import init_app
from kanban.api import api


def create_app(cfg=None):
    app = Flask(__name__)  # create the application instance :)
    app.config.from_mapping(
        DEBUG=True,
        DEVELOPMENT=True,
        SECRET_KEY="development key",
        DATABASE=os.path.join(app.root_path, "kanban.db"),
    )  # load config
    if cfg:
        app.config.update(cfg)  # update config as necessary

    init_app(app)
    app.register_blueprint(api)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
