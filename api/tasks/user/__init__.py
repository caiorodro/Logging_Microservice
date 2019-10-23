from flask_restful import Api
from mainUser import flaskApp
from api.tasks.user.taskUser import taskUser

restServer = Api(flaskApp)

restServer.add_resource(taskUser, "/api/v1.0/taskUser")
