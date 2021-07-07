#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3

import os
import MySQLdb as mdb

import json


class Database():
    def __init__(self):
        self.connected = False


    def connect(self):
        if not self.connected:
            credencials = self.authenticate()
            address = credencials.get('DatabaseAddress')
            name = credencials.get('DatabaseName')
            user = credencials.get('DatabaseUser')
            password = credencials.get('DatabaseUserPass')

            try:
                self.bank = mdb.connect(address, user, password, name, port=3306)
            except:
                self.conected = False
                raise
            else:
                self.cursor = self.bank.cursor()
                self.conected = True

        return {
            'Database' : self.bank,
            'Cursor'   : self.cursor
        }

    
    def disconnect(self):
        if self.connected:
            try:
                self.bank.close()
            except:
                raise Exception('Database connection not initialized')
        
        self.conected = False
        return True


    def authenticate(self):
        """
        Utiliza as informações presentes no config para\n
        retorná-las em forma de lista como credenciais
        Retorno -> Lista:\n
        [0] IP banco, [1] Usuario Banco\n
        [2] Senha Usuario, [3] Nome Banco
        """
        with open('config.json', 'r') as config:
            config = json.loads(
                config.read()
            )
            
        config = config['database']

        db_address = config.get('dbAddress')
        db_user = config.get('dbUser')
        db_name = config.get('dbName')
        db_user_password = config.get('dbPass')
        if db_user_password is None:
            if os.environ.get('db_pass') is not None:
                db_user_password = os.environ.get('db_pass')
            else:
                db_user_password = ''
        
        return {
            'DatabaseAddress' : db_address,
            'DatabaseName' : db_name,
            'DatabaseUser' : db_user,
            'DatabaseUserPass' : db_user_password
        }


    def execute_with_commit(self, query):
        self.connect()
        try:
            self.cursor.execute(query)
        except:
            raise
        else:
            self.bank.commit()
            self.disconnect()
            return True


    def execute_with_return(self, query, header=None):
        results = None
        
        self.connect()
        try:
            self.cursor.execute(query)
        except:
            raise
        else:
            results = list(self.cursor.fetchall())
            
            if header:
                for _, result in enumerate(results):
                    results[_] = {f'{header[x]}':result[x] for x in range(len(header))}
                
            self.disconnect()

        return results


    def parameters_parse(self, query, parameters={}):
        try:
            with open(query, 'r') as sql:
                query = " ".join(sql.read().split())
                
            for parameter in parameters.keys():
                query = query.replace('{'+parameter+'}', parameters[parameter])
        except:
            raise
        return query


    def return_columns(self,  table):
        columns = self.execute_with_return('show tables')
        
        dict_columns = {}

        for column in columns:
            dict_columns[column[0]] = [column[x+1] for x in range(len(column[1:]))]

        return dict_columns
