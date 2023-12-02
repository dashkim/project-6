"""
Resource: Brevet
"""
from flask import request, Response
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError

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


class Brevet(Resource):
    def get(self, brevet_id: str):
        """Get a single brevet from the database."""
        try:
            # Retrieve a single brevet by ID and return it as JSON
            brevet = Brevet.objects.get(id=brevet_id)
            return Response(brevet.to_json(), mimetype="application/json", status=200)
        except ValidationError as exc:
            # Handle validation errors (e.g., invalid ID format)
            return {"error": str(exc)}, 400
        except DoesNotExist:
            return {"error": f"No brevet found for id {brevet_id}."}, 404
        except Exception as exc:
            # Handle unexpected errors
            return {"error": str(exc)}, 500

    def put(self, brevet_id: str):
        """Replace a single brevet in the database."""
        try:
            # Validate the new document before updating
            Brevet(**request.json).validate()
            
            # Update the brevet with the new data from request.json
            docs_updated = Brevet.objects.get(id=brevet_id).update(
                __raw__={"$set": request.json}
            )
            
            # Check if exactly one document was updated
            if docs_updated == 1:
                return {"success": True}, 200
            else:
                return {"error": "The document may or may not have been updated."}, 500
        except DoesNotExist:
            return {"error": str(exc)}, 404
        except ValidationError as exc:
            # Handle validation errors for the new document            
            return {"error": str(exc)}, 400
        except Exception as exc:
            # Handle unexpected errors
            return {"error": str(exc)}, 500

    def delete(self, brevet_id: str):
        """Delete a single brevet from the database."""
        try:
            # Delete the brevet by ID
            Brevet.objects.get(id=brevet_id).delete()
            return {"success": True}, 200
        except DoesNotExist:
            return {"error": str(exc)}, 404
        except ValidationError as exc:
            # Handle validation errors (e.g., invalid ID format)
            return {"error": str(exc)}, 400
        except Exception as exc:
            # Handle unexpected errors
            return {"error": str(exc)}, 500