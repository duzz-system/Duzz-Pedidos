from flask_restful import Resource

from resources.models.database import Database

class Pedidos(Resource):
    def get(self):
        return {
            'codigo': 1
        }
    
    
    def put(self):
        pass    
    
    
    def post(self):
        pass
    
    
    def delete(self):
        pass