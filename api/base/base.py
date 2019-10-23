from flask import jsonify
import json
from decimal import Decimal

class Base:

    @staticmethod
    def toJsonRoute(self, message, status=int):
        return jsonify({ "message": message }), status

    @staticmethod
    def threatColunms(row):
        isStr = type(row) is str

        if not isStr:
            retorno = list(row)

            for i, item in enumerate(retorno):
                if type(retorno[i]) == str:
                    retorno[i] = retorno[i].replace('"', '') 
                elif type(retorno[i]) == int:
                    pass
                elif type(retorno[i]) == Decimal:
                    retorno[i] = float(item)
        elif isStr:
            retorno = row.replace('"', '') 

        return retorno
    @staticmethod
    def toJson(lista):
        lista1 = []
        lista1.extend(list(map(Base.threatColunms, lista)))
        return json.dumps(lista1)
