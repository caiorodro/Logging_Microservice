import json
from flask import jsonify
import requests
import traceback
import unittest
from api.base.loggerNoSQL import kindOfLog

class user(unittest.TestCase):

    def __init__(self):
        self.__listOfUsers = []
        self.__idUser = 1
        self.__recUser = 0

        super(user, self).__init__()

    def listUsers(self):

        self.__listOfUsers.append({
            "ID_USER": 1,
            "USER_NAME": "Caio Rodrigues",
            "EMAIL": "caiorodro@gmail.com"
        })

        self.__newLog(f'User list was performed.', kindOfLog.INFO(), '', self.__idUser)

        return len(self.__listOfUsers)

    def saveUser(self, ID_USER, USER_NAME, EMAIL):

        try:
            self.__newLog(f'User data successfuly saved. {ID_USER}, {USER_NAME}, {EMAIL}', kindOfLog.INFO(), '', 
                self.__idUser)
            return True
        except Exception as ex:
            self.__newLog(ex.args[0], kindOfLog.ERROR(), traceback.format_exc(), self.__idUser)

            return False

    def testListOfUsers(self):
        try:
            self.assertGreater(self.listUsers(), 0)

            return { "message": "Ok", "result": self.__listOfUsers }, 200

        except AssertionError as ae:
            _message = ae.args[0]

            return { "message": "Error", "result": _message }, 500

    def testSaveUser(self, ID_USER, USER_NAME, EMAIL):
        try:
            self.assertTrue(self.saveUser(ID_USER, USER_NAME, EMAIL))
            
            return { "message": "Ok", 
                "result": f'User data successfuly saved. {ID_USER}, {USER_NAME}, {EMAIL}' }, 200
        except AssertionError as ae:
            _message = ae.args[0]

            return { "message": "Error", "result": ae.args[0] }, 500

    def __newLog(self, message, kind, trace, idUser):
        try: 
            URL = 'http://127.0.0.1:5005/api/v1.0/taskLogger'

            PARAMS = { "message": message, "kind": kind, "trace": trace, "idUser": idUser }

            result = requests.put(url=URL, json=PARAMS)

            self.assertEqual(result.status_code, 200)
        except AssertionError:
            pass

    def __del__(self):
        pass