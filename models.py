from pony.orm import Database, Required, Set, Optional, PrimaryKey

db = Database()

class Flower(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    color = Required(str)
    price = Required(float)
    image_link = Optional(str) 
    amount = Required(int)
    orders = Set('OrderFlower') 

class Order(db.Entity):
    email = Required(str)
    phone_number = Required(str)
    type = Required(str)
    delivery = Required(bool)
    greenery = Required(bool)
    tape = Required(bool)
    paper = Required(bool)
    message = Optional(str)
    address = Optional(str)
    time = Required(str)
    gdrp = Required(bool)
    flower_ids = Set('OrderFlower')

class OrderFlower(db.Entity):
    id = PrimaryKey(int, auto=True)
    order = Required(Order)
    flower = Required(Flower)
    quantity = Required(int)

db.bind(provider='sqlite', filename='lapo.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

