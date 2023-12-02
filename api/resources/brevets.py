"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
from mongoengine.errors import ValidationError

from database.models import Brevet

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.


class Brevets(Resource):
    def get(self):
        """Get all brevets stored in the database."""
        try:
            # Retrieve all brevets and convert to JSON
            brevets_json = Brevet.objects.to_json()
            return Response(brevets_json, mimetype="application/json", status=200)
        except Exception as exc:
            # Handle unexpected errors
            return {"error": str(exc)}, 500

    def post(self):
        """Create a new brevet in the database."""
        try:
            # Create a new brevet from the JSON data in the request and save it
            new_brevet = Brevet(**request.json).save(validate=True)
            # Return the ID of the newly created brevet
            return {"id": str(new_brevet.id)}, 201
        except ValidationError as exc:
            # Handle validation errors
            return {"error": str(exc)}, 400
        except Exception as exc:
            # Handle unexpected errors
            return {"error": str(exc)}, 500