from peewee import CharField
from BaseModel import BaseModal

class Ticket(BaseModal):
    subject = CharField()
    description = CharField()
    user_id = CharField()
    created_at = 
