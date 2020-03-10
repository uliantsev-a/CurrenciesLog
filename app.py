from sqlalchemy import exc

from project import app
from project.loader import run_load_currencies
from project.fixtures import make_test_user, make_default_currency


@app.cli.command()
def load():
    run_load_currencies()


@app.cli.command()
def first_filling():
    try:
        make_default_currency()
    except exc.IntegrityError:
        app.logger.error("first-filling should run only first running")


@app.cli.command()
def test_user():
    try:
        make_test_user()
    except exc.IntegrityError:
        app.logger.error("test user already exists, try enter with test:test")


def main():
    app.run()


if __name__ == '__main__':
    main()
