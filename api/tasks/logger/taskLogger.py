from flask_restful import Resource
from flask import request
import json

from api.base.loggerNoSQL import loggerNoSQL

class taskLogger(Resource):

    def __init__(self):
       pass

    def get(self):
        rec = request.get_json(force=True)

        start = rec['start']
        limit = rec['limit']
        _date = rec['date']

        log = loggerNoSQL()
        result = log.testListLogs(_date, start, limit)
        del log

        return result

    def put(self):
        rec = request.get_json(force=True)

        idUser = rec['idUser']
        message = rec['message']
        kind = rec['kind']
        trace = rec['trace']

        log = loggerNoSQL()
        result = log.testAddLog(message, kind, trace, idUser)
        del log

        return result

    def post(self):
        return { "message": "Error", "result": "POST method not implemented" }, 500

    def delete(self):
        return { "message": "Error", "result": "DELETE method not implemented" }, 500
