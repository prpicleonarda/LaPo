from flask import Blueprint, request, render_template, redirect, url_for
from pony.orm import db_session
from models import Flower, Order, OrderFlower

bp = Blueprint('main', __name__)

# ADDING THE ROUTES & NEEDED FUNCTIONS
