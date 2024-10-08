from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from pony.orm import db_session
from models import Flower, Order, OrderFlower

bp = Blueprint('main', __name__)

@bp.route('/')
@db_session
def index(): 
    flowers = Flower.select()[:]
    return render_template('index.html', flowers = flowers)

@bp.route('/flowers/add', methods=['GET', 'POST'])
@db_session
def add_flower():
    if request.method == 'POST':
        name = request.form['flower_type']
        color = request.form['color']
        price = float(request.form['price'])
        amount = int(request.form['amount'])
        image_link = request.form.get('image_link')

        Flower(name=name, color=color, price=price, amount=amount, image_link=image_link)
        return redirect('/view_orders')
    return render_template('add_flower.html')

@bp.route('/flowers/edit/<int:id>', methods=['GET', 'POST'])
@db_session
def edit_flower(id):
    flower = Flower.get(id=id)
    if not flower:
        return "Flower not found", 404

    if request.method == 'POST':
        flower.name = request.form['flower_type']
        flower.color = request.form['color']
        flower.price = float(request.form['price'])
        flower.amount = int(request.form['amount'])
        flower.image_link = request.form.get('image_link')
        return redirect('/view_orders')

    return render_template('edit_flower.html', flower=flower)

@bp.route('/flowers/delete/<int:id>', methods=['POST'])
@db_session
def delete_flower(id):
    flower = Flower.get(id=id)
    if not flower:
        return "Flower not found", 404

    flower.delete()
    return redirect('/view_orders')

@bp.route('/orders/edit/<int:id>', methods=['GET', 'POST'])
@db_session
def edit_order(id):
    order = Order.get(id=id)
    if not order:
        return "Order not found", 404

    if request.method == 'POST':
        order.email = request.form['email']
        order.phone_number = request.form['phone_number']
        order.type = request.form['type']
        order.address = request.form['address']
        order.time = request.form['time']
        order.message = request.form['message']
        order.delivery = request.form.get('delivery') == 'on'
        order.greenery = request.form.get('greenery') == 'on'
        order.tape = request.form.get('tape') == 'on'
        order.paper = request.form.get('paper') == 'on'
        order.gdrp = request.form.get('gdrp') == 'on'
        return redirect('/view_orders')

    return render_template('edit_order.html', order=order)

@bp.route('/orders/delete/<int:id>', methods=['POST'])
@db_session
def delete_order(id):
    order = Order.get(id=id)
    if not order:
        return "Order not found", 404

    order.delete()
    return redirect('/view_orders')

@bp.route('/view_orders')
@db_session
def view_orders_and_flowers():
    orders = Order.select()[:]
    flowers = Flower.select()[:]
    return render_template('view_orders.html', orders=orders, flowers=flowers)

@bp.route('/orders/new', methods=['GET', 'POST'])
@db_session
def add_order():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'submit_order':
            try:
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                order_type = request.form.get('type')
                delivery = request.form.get('delivery') == 'on'
                greenery = request.form.get('greenery') == 'on'
                tape = request.form.get('tape') == 'on'
                paper = request.form.get('paper') == 'on'
                message = request.form.get('message')
                address = request.form.get('address')  
                time = request.form.get('datetime')  # 'datetime' instead of 'time'
                gdrp = request.form.get('gdrp') == 'on'

                # Create the order
                order = Order(email=email, phone_number=phone_number, type=order_type, delivery=delivery,
                              greenery=greenery, tape=tape, paper=paper, message=message, address=address,
                              time=time, gdrp=gdrp)

                # Handle flowers
                flower_ids = request.form.getlist('flower_id[]')
                flower_quantities = request.form.getlist('flower_quantity[]')

                for flower_id, quantity in zip(flower_ids, flower_quantities):
                    if flower_id and quantity:
                        flower = Flower.get(id=int(flower_id))
                        if flower:
                            quantity = int(quantity)
                            if flower.amount >= quantity:
                                OrderFlower(order=order, flower=flower, quantity=quantity)
                                flower.amount -= quantity
                            else:
                                # Pass the error message to the template
                                error_message = f"Please reduce the quantity. There are only {flower.amount} {flower.name}(s) left."
                                flowers = Flower.select()
                                selected_flowers = list(zip(flower_ids, flower_quantities))
                                return render_template('add_order.html', flowers=flowers, selected_flowers=selected_flowers, error_message=error_message)
                        else:
                            error_message = "Invalid flower ID."
                            flowers = Flower.select()
                            selected_flowers = list(zip(flower_ids, flower_quantities))
                            return render_template('add_order.html', flowers=flowers, selected_flowers=selected_flowers, error_message=error_message)

                return redirect('/view_orders')

            except Exception as e:
                print(f"An error occurred: {e}")
                error_message = "An error occurred while processing the order."
                flowers = Flower.select()
                selected_flowers = list(zip(flower_ids, flower_quantities))
                return render_template('add_order.html', flowers=flowers, selected_flowers=selected_flowers, error_message=error_message)

    else:
        flowers = Flower.select()
        selected_flowers = [('', 1)]
        return render_template('add_order.html', flowers=flowers, selected_flowers=selected_flowers)
