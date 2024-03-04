from flask import Flask
from flask_cors import CORS
from controllers.app_controller import main_blueprint
from controllers.microcontroller_controller import microcontroller_blueprint

app = Flask(__name__, static_url_path='/static', template_folder='views')
CORS(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(microcontroller_blueprint)

if __name__ == '__main__':
    app.run(debug=True, port=4000, host='0.0.0.0')
