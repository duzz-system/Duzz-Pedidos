from resources.models.database import Database
from resources.models import Models


class ModelPedidos:
    def __init__(self):
        self.database = Database()
        self.models = Models()
        
    
    def novo(self):
        pass
    
    
    def editar(self):
        pass
    
    
    def excluir(self):
        pass
    
    
    def pesquisar(self, data):
        data = self.models.body_validate(
            data, {
                'id': {
                    'required': False,
                    'type': int
                },
                'lanches': {
                    'required': False,
                    'type': str
                },
                'cliente': {
                    'required': False,
                    'type': str
                },
                'status': {
                    'required'
                }
            }
        )
        
        if not data:            
            pedidos = self.database.execute_with_return(
                '''
                SELECT
                    *
                FROM 
                    `pedidos` 
                ''', self.database.return_columns('pedidos')
            )
        else:
            if data.get('id') is not None:
                pedidos = self.database.execute_with_return(
                f'''
                SELECT
                    *
                FROM 
                    `pedidos`
                WHERE
                    id = {data["id"]}  
                ''', self.database.return_columns('pedidos')
            )
                
            else:
                
                
        