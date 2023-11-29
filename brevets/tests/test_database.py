"""
Nose tests for flask_brevets.py/Mongo Implementation

Write your tests HERE AND ONLY HERE.
"""
import arrow
import requests
from pymongo import MongoClient
from nose.tools import assert_true, assert_equal

mongo = MongoClient('mongodb://mongodb', 27017)
collection = mongo.collection

# Update the URL to match your Flask app's address
BASE_URL = "http://localhost:5000"

def test_insertion_and_retrieval():
    # Test data for insertion
    test_doc = {
        "full_dist": "800",
        "start_time": "2021-01-01T00:00",
        "controls": [{"300": "B"}]
    }

    # Insert the test document
    response = requests.post(f"{BASE_URL}/_submit", json=test_doc)
    assert_equal(response.status_code, 500, f"Insertion status code was {response.status_code}.")

    # Retrieve the inserted document
    retrieved_doc = requests.get(f"{BASE_URL}/_retrieve_brevet").json()

    # Check if the document exists
    assert_true(document_exists(test_doc), "No document found")

    # Compare the inserted and retrieved documents
    assert_equal(test_doc, retrieved_doc, "Inserted and retrieved documents do not match.")

def document_exists(doc):
    # Check if the document exists in MongoDB
    return collection.controls.find_one(doc) is not None

# Optionally add a teardown method to clean up the test data
def teardown_module():
    collection.controls.delete_many({"full_dist": "800"})

# Run the tests
if __name__ == '__main__':
    import nose
    nose.runmodule()
