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
        image_link = request.form.get('image_link')

        Flower(name=name, color=color, price=price, image_link=image_link)
        return redirect(url_for('main.view_flowers'))
    return render_template('add_flower.html')

@bp.route('/view_flowers')
@db_session
def view_flowers():
    flowers = Flower.select()[:]
    return render_template('view_flowers.html', flowers=flowers)

