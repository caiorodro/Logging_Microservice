from flask_restful import Resource
from flask import request

from api.tasks.user.user import user

class taskUser(Resource):

    def __init__(self):
       pass

    def get(self):
        print('Ok')
        rec = request.get_json(force=True)
        idUser = rec['idUser']

        result = user().testListOfUsers()

        return result

    def put(self):
        rec = request.get_json(force=True)
        
        ID_USER = rec['ID_USER']
        USER_NAME = rec['USER_NAME']
        EMAIL = rec['EMAIL']

        result = user().testSaveUser(ID_USER, USER_NAME, EMAIL)

        return result

    def post(self):
        return { "message": "Error", "result": "POST method not implemented" }, 500

    def delete(self):
        return { "message": "Error", "result": "DELETE method not implemented" }, 500