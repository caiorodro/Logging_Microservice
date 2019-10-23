from datetime import datetime
import unittest

from pymongo import MongoClient, errors
import traceback

class loggerNoSQL(unittest.TestCase):

    def __init__(self):
        """
        Class that write and read logging on any kind info or error of the application
        """
        self.client = MongoClient("mongodb+srv://admin:100grillo@cluster0-sh419.mongodb.net/test?retryWrites=true&w=majority")
        self.idsInserted = []

        self.__testConnection()

        self.__listOfLogs = []

    def checkServer(self):
        """
        Try to connect on MongoDB cloud instance and try to create collections

        Return: True if the database is reachable and False on any problem encontered on that
        """
        try:
            self.client.server_info()
            self.db = self.client.logRecipe
            self.__startTables()

            return True
        except:
            return False

    def __testConnection(self):
        """
        Tests the checkserver method to connect on database
        """

        try:
            self.assertTrue(self.checkServer(), True)
        except AssertionError as ae:
            raise Exception('Failure to connect in database. \n',
                ae.args[0])

    def addLog(self, message, kind, trace, idUser):
        """
        Creates a new log info or error and insert on database
        """

        tb_logInfo = self.db.tb_logInfo

        result = tb_logInfo.insert_one({
            'ID_USER': idUser,
            'DATE_OF': datetime.now().strftime('%m/%d/%Y %H:%M'),
            'MESSAGE': message,
            'LEVEL': kind,
            'TRACE': trace
        })

        return result._WriteResult__acknowledged

    def listLogs(self, _date, start, limit):
        """
        Creates a filtered list of collextion logs

        Return: returns a length of records found
        """
        tb_logInfo = self.db.tb_logInfo

        recipes = tb_logInfo.find({
            'DATE_OF': { '$gt': _date }
        }).sort('DATE_OF', -1).skip(start).limit(limit)

        for item in recipes:
            self.__listOfLogs.append((item['DATE_OF'], item['LEVEL'], item['MESSAGE'], item['TRACE']))

        return len(self.__listOfLogs)

    def testAddLog(self, message, kind, trace, idUser):
        """
        Tests the addLog method

        Return: returns number of inserted record(s). One record will inserted by default
        """

        try:
            self.assertGreater(self.addLog(message, kind, trace, idUser), 0)

            return { "message": "Ok", "result": "1 record of Logging was inserted on the database" }, 200
        except AssertionError as ae:
            return { "message": "Error", "result": ae.args[0] }, 500

    def testListLogs(self, data, start, limit):
        """
        Tests the list of logs

        Return: returns the listOfLogs filled list 
        """

        try:
            self.assertGreater(self.listLogs(data, start, limit), 0)

            return { "message": "Ok", "result": self.__listOfLogs }, 200
        except AssertionError as ae:
            return { "message": "Error", "result": ae.args[0] }, 500

    def __startTables(self):
        """
        Starts to create table collections if they don't created yet
        """

        tables = [{ "tableName": "tb_logInfo",
                   "firstRec": {
                       "ID_USER": 1,
                        "DATE_OF": datetime.now().strftime('%m/%d/%Y %H:%M'),
                        "MESSAGE": "Test log",
                        "LEVEL": 'INFO',
                        "TRACE": "Empty"
                    }
                }, { "tableName": "tb_user",
                   "firstRec": {
                        "ID_USER": 1,
                        "EMAIL": "caiorodro@gmail.com",
                        "NAME": "Caio Rodrigues"
                    }
                }]

        for item in tables:
            self.__createTable(item['tableName'], item['firstRec'])

    def __createTable(self, tableName, firstRec):
        """
        Checks if tableName is created and do the table with fields
        described in firstRec variable if don't.

        Return: 
            returns True if table was successfully created
        """
        if tableName not in self.db.collection_names():
            tbl = self.db[tableName]
            tbl.insert_one(firstRec)
            tbl.delete_one(firstRec)

            return True

        return False

class kindOfLog:
    
    @staticmethod
    def ERROR():
        return 'ERROR'

    @staticmethod
    def INFO():
        return 'INFO'
