from flask_restful import Api
from mainLogger import flaskApp
from api.tasks.logger.taskLogger import taskLogger

restServer = Api(flaskApp)

restServer.add_resource(taskLogger, "/api/v1.0/taskLogger")
