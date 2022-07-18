from peewee import *

db = SqliteDatabase("betsy.db")

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    user_id = AutoField(unique=True)
    name = CharField(max_length=50, null=False, index=True)
    street = CharField(max_length=50, null=False, index=True)
    zip_code = CharField(max_length=7, null=False, index=True)
    city = CharField(max_length=30, null=False, index=True)
    billing_info = CharField()
    class Meta:
        database = db

class Products(BaseModel):
    product_id = AutoField(unique=True)
    owner = ForeignKeyField(Users)
    name = CharField(null=False, index=True)
    desc = TextField(null=False, index=True)
    price = DecimalField(
        auto_round=False, decimal_places=2, max_digits=6, null=False, constraints=[Check('price > 0')])
    stock = IntegerField()
    class Meta:
        database = db

class Tags(BaseModel):
    tag_id = AutoField(unique=True)
    name = CharField(null=False)
    class Meta:
        database = db

class ProductTag(BaseModel):
    producttag_id = AutoField()
    product = ForeignKeyField(Products)
    tag = ForeignKeyField(Tags)
    class Meta:
        database = db

class Transactions(BaseModel):
    transaction_id = AutoField(unique=True)
    buyer = ForeignKeyField(Users)
    purchased_product = ForeignKeyField(Products)
    purchased_quantity = IntegerField()
    purchased_price = IntegerField()
    date = DateField(formats='%d-%m-%Y')

    class Meta:
        database = db