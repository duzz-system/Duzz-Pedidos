from werkzeug.exceptions import BadRequest
from datetime import datetime


class Models:
    def body_validate(self, body, header, minLen=None, maxLen=None):
        body = {} if not body else body
        
        if not isinstance(body, dict):
            body = self.get_dict_from_json(body)
            
        if minLen:
            if len(body) < minLen:
                raise BadRequest(message='O tamanho do body é menor que o mínimo permitido')
        if maxLen:
            if len(body) > maxLen:
                raise BadRequest(message='O tamanho do body é maior que o mínimo permitido')
    
        for item in header:
            if header[item]['required']:
                try:
                    body[item]
                except KeyError:
                    raise BadRequest

        for item in body.keys():
            if item not in header.keys():
                raise BadRequest
            
            if not isinstance(body[item], header[item]['type']):
                if header[item]['type'] is datetime:
                    if isinstance(body[item], str):
                        dateFormat = header[item].get('dateFormat')
                        
                        dateFormat = dateFormat if dateFormat else '%Y%m%d%H%M%S'
                        
                        body[item] = datetime.strptime(body[item], dateFormat)
                elif header[item]['type'] is dict:
                    if isinstance(body[item], str):
                        body[item] = self.get_dict_from_json(body[item])
                    else:
                        raise BadRequest(f'não foi possivel converter o {item} à objeto')
                elif type(body[item]) is bool:
                    try:
                        if isinstance(body[item], str):
                            if 'false' in body[item].lower():
                                body[item] = False
                            elif 'true' in body[item].lower():
                                body[item] = True
                            else:
                                body[item] = bool(int(body[item]))  
                    except:
                        raise BadRequest
                elif type(body[item]) is str:
                    try:
                        body[item] = header[item]['type'](body[item])
                    except:
                        raise BadRequest
                else:
                    try:
                        body[item] = header[item]['type'](body[item])
                    except:
                        raise BadRequest

        return body