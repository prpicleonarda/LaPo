Order { flower id, email, phone_number, type, delivery, greenery, tape, paper, message, address, time, delivery, gdrp }
Flowers { name, color, type, amount, image_link }

Order can have many different flowers
Flowers can be in many different orders

Needs to have a middle class OrderFlowers which saves how many flowers are in the order
