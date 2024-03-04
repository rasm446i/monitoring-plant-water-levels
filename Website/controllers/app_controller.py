from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def home():
    return render_template('home.html', active_page='home')


@main_blueprint.route('/floorplan')
def floorplan():
    return render_template('floorplan.html', active_page='floorplan')


@main_blueprint.route('/settings')
def settings():
    return render_template('settings.html', active_page='settings')
