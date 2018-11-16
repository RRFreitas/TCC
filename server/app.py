from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from server.common.database import db
from server.resources.PessoaResource import PessoaResource
import sys
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db.init_app(app)

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api')

api.add_resource(PessoaResource, '/pessoas', '/pessoas/<int:pessoa_id>')

app.register_blueprint(api_bp)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def run(host='0.0.0.0', debug=False):
    port = int(os.environ.get("PORT", 5000))
    app.debug = debug
    app.run(host=host, port=port)

if __name__ == "__main__":
    run(debug='-d' in sys.argv or '--debug' in sys.argv)