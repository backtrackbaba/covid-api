import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=os.environ.get('POSTGRESQL_USERNAME'),
        pw=os.environ.get('POSTGRESQL_PASSWORD'),
        url=os.environ.get('POSTGRESQL_URL'),
        db=os.environ.get('POSTGRESQL_DATABASE'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
