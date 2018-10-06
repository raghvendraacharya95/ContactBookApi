from flask import Flask
from api_controllers import api

application = Flask(__name__)
api.init_app(application)

# application.run(debug=True)