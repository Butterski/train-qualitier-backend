from flask import Flask
import logging


def create_app():
    app = Flask(__name__)
    return app


if __name__ == '__main__':

    app = create_app()
    logger = logging.getLogger(__name__)

    app.run(host="0.0.0.0", debug=True)