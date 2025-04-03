from peewee import BooleanField, CharField, DateTimeField
from models.BaseModel import BaseModal
from datetime import datetime

class Ticket(BaseModal):
    subject = CharField()
    description = CharField()
    user_id = CharField()
    resolution = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
