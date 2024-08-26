from flask import Blueprint, request, render_template, redirect, url_for
from pony.orm import db_session
from models import Flower, Order, OrderFlower

bp = Blueprint('main', __name__)

@bp.route('/add_flower', methods=['GET', 'POST'])
@db_session
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        price = float(request.form['price']) 
        amount = int(request.form['amount'])
        image_link = request.form.get('image_link')

        Flower(name=name, color=color, price=price, amount=amount, image_link=image_link)
        return redirect(url_for('main.view_orders'))
    return render_template('add_flower.html')

@bp.route('/view_orders')
@db_session
def view_orders():
    flowers = Flower.select()[:]
    return render_template('view_orders.html', flowers=flowers)
def view_orders():
    orders = Order.select()
    return render_template('view_orders.html', orders=orders)
@bp.route('/orders/new', methods=['GET', 'POST'])
@db_session
def add_order():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'submit_order':
            try:
                # Process the form submission
                email = request.form.get('email')
                phone_number = request.form.get('phone_number')
                order_type = request.form.get('type')
                delivery = request.form.get('delivery') == 'on'
                greenery = request.form.get('greenery') == 'on'
                tape = request.form.get('tape') == 'on'
                paper = request.form.get('paper') == 'on'
                message = request.form.get('message')
                address = request.form.get('address')
                time = request.form.get('time')
                gdrp = request.form.get('gdrp') == 'on'
                
                # Create a new order
                order = Order(email=email, phone_number=phone_number, type=order_type, delivery=delivery,
                              greenery=greenery, tape=tape, paper=paper, message=message, address=address,
                              time=time, gdrp=gdrp)

                # Gather flower data
                flower_ids = request.form.getlist('flower_id[]')
                flower_quantities = request.form.getlist('flower_quantity[]')

                for flower_id, quantity in zip(flower_ids, flower_quantities):
                    if flower_id and quantity:
                        flower = Flower.get(id=int(flower_id))
                        if flower and flower.amount >= int(quantity):
                            OrderFlower(order=order, flower=flower, quantity=int(quantity))
                            flower.amount -= int(quantity)  # Update flower amount
                        else:
                            return "Invalid flower ID or quantity exceeds available amount.", 400

                return redirect(url_for('main.view_orders'))

            except Exception as e:
                # Log or print the exception for debugging purposes
                print(f"An error occurred: {e}")
                return "An error occurred while processing the order.", 500

    else:
        # Initial form load
        flowers = Flower.select()
        selected_flowers = [('', 1)]  # Start with one empty flower selection
        return render_template('add_order.html', flowers=flowers, selected_flowers=selected_flowers)
