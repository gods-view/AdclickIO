from peewee import *
from .config import mysql

db = MySQLDatabase(mysql['name'], host=mysql['host'], port=int(
    mysql['port']), user=mysql['user'], passwd=mysql['passwd'])


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db


class PProvider(BaseModel):
    name = CharField(null=False)

    class Meta:
        db_table = "providers"
        indexes = (
            (('name'), True),
        )


class PApiToken(BaseModel):
    token = CharField(null=False)
    username = CharField()
    password = CharField()
    userId = CharField()
    initialized = BooleanField(default=False)
    provider = ForeignKeyField(PProvider)

    class Meta:
        db_table = "api_tokens"
        indexes = (
            (('token', 'username', 'password', 'provider_id', 'userId'), True),
        )

class PCampaign(BaseModel):
    name = CharField(null=False)
    campaign_identity = CharField(null=False)
    provider = ForeignKeyField(PProvider)
    api_token = ForeignKeyField(PApiToken)

    class Meta:
        db_table = "campaigns"
        indexes = (
            (('provider_id', 'campaign_identity'), True),
        )


class PStatistics(BaseModel):
    cost = FloatField(default=0)
    impression = IntegerField(default=0)
    click = IntegerField(default=0)
    conversion = IntegerField(default=0)
    date = DateField(null=False)
    provider = ForeignKeyField(PProvider)
    campaign = ForeignKeyField(PCampaign)
    api_token = ForeignKeyField(PApiToken)

    class Meta:
        db_table = 'statistics'
        indexes = (
            (('date', 'provider_id', 'campaign_id'), True),
        )


db.connect()
