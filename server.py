from logging import debug
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources import (
    Pedidos
)

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/')
def index():
    return """
        <h1> Hello World!
        """
        
api.add_resource(Pedidos, '/pedidos')

if __name__ == '__main__':
    app.run(debug=True)