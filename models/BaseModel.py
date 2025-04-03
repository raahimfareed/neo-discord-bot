from peewee import Model
from database import db

class BaseModal(Model):
    class Meta:
        database = db


