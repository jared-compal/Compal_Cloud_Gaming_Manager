from flask import Blueprint, render_template, redirect
from flask_login import login_required


backstage = Blueprint('backstage', __name__, template_folder='backstage/templates', static_folder='static')


@backstage.route('/')
@login_required
def backstage_home():
    render_template('index.html', games=None, streams=None)
