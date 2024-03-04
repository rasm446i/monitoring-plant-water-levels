from flask import Blueprint, render_template
from models.microcontroller import microcontrollers

microcontroller_blueprint = Blueprint('microcontroller', __name__)


@microcontroller_blueprint.route('/microcontroller/<microcontroller_id>')
def microcontroller(microcontroller_id):
    print(f"Requested Microcontroller ID: {microcontroller_id}")
    if microcontroller_id in microcontrollers:
        return render_template('microcontroller.html', microcontroller=microcontrollers[microcontroller_id])
    else:
        return "Microcontroller not found."
