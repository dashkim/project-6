"""
Brevets RESTful API
"""
from os import environ as env
from flask import Flask
from flask_restful import Api
import flask_cors
from mongoengine import connect

from resources.brevet import Brevet
from resources.brevets import Brevets

URL = "http://localhost:5002"

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{env['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
api = Api(app)
 
# Bind resources to paths here:
api.add_resource(Brevet, "/api/brevet/<string:brevet_id>")
api.add_resource(Brevets, "/api/brevets")

if __name__ == "__main__":
    # Run flask app normally
    print(f"Open on port {env['PORT']}")
    # Enables communication between ports
    cors = flask_cors.CORS(app, resources={r"/api/*": {"origins": URL}}) 
    app.run(port=int(env["PORT"]), host="0.0.0.0")