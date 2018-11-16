import os
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

DEBUG = True

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_DATABASE_URI = config['DEV']['elephan_auth']
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = config['DEV']['secret_key']