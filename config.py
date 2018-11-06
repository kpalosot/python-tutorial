import os

class Config(object):
  SECRET_key = os.environ.get('SECRET_KEY') or 'you-will-never-guess'