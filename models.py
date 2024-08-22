from pony.orm import Database, Required, Set, Optional, PrimaryKey

db = Database()
 
#TODO: Define the Flower class here

#TODO: For this to work there needs to be a Flower class defined
#
# class Order(db.Entity):
#    email = Required(str)
#    phone_number = Required(str)
#    type = Required(str)
#    delivery = Required(bool)
#    greenery = Required(bool)
#    tape = Required(bool)
#    paper = Required(bool)
#    message = Optional(str)
#    address = Required(str)
#    time = Required(str)
#    gdrp = Required(bool)
#    # Many-to-many relationship with Flower through OrderFlower
#    flower_ids = Set('OrderFlower')
#

#TODO: Add the OrderFlower class here

# Bind the database to a file named lapo.sqlite; TODO: Uncomment this when the Flower class is defined and the OrderFlower class is defined
db.bind(provider='sqlite', filename='lapo.sqlite', create_db=True)

# Generate the tables
db.generate_mapping(create_tables=True)

##IF ERROR DELETE THE lapo.sqlite FILE AND RUN THE APP AGAIN
