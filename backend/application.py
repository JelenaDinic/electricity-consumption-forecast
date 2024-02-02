from flask import Flask
from flask_cors import CORS
import sys
sys.path.append('../')
app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

from controller_example import *

if __name__ == '__main__':
    app.run(port=5000,debug=True)