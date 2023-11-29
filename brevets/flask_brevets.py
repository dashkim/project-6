"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import flask
import arrow # Replacement for datetime, based on moment.js
import acp_times # Brevet time calculations
import config
import logging
import os
from pymongo import MongoClient
from secrets import token_hex as gen_secret_key

###
# Globals
###

app = flask.Flask(__name__)
CONFIG = config.configuration()

mongo = MongoClient('mongodb://mongodb', 27017)
collection = mongo.collection
app.secret_key = gen_secret_key()


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    if "client_id" not in flask.session:
        flask.session["client_id"] = gen_secret_key()
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(_):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.get("/_calc_times")
def calculate_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects three query parameters: 'brevet' (integer), 'control' (float), and 'start' (ISO 8601 timestamp).
    """
    app.logger.debug("Got a JSON request")

    brevet_dist = flask.request.args.get('brevet', type=int)
    control_dist = flask.request.args.get('control', type=float)
    start_time = flask.request.args.get('start')

    try:
        brevet_dist = int(brevet_dist)
        control_dist = float(control_dist)
        start_time = arrow.get(start_time)
    except (ValueError, TypeError):
        return flask.jsonify({"error": "Invalid parameters."}), 400

    open_time, close_time = None, None

    try:
        open_time = acp_times.open_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
        close_time = acp_times.close_time(control_dist, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    except ValueError as exc:
        return flask.jsonify({"error": str(exc)}), 400
    except Exception:
        return flask.jsonify({"error": "A server error occurred."}), 500

    return flask.jsonify({"open": open_time, "close": close_time})


#############



@app.post('/_submit')
def submit():
    try:
        collection.controls.update_one(
            {"session": flask.session["client_id"]},
            {"$set": flask.request.json},
            upsert=True
        )
        return {"success": True}
    except ValueError as exc:
        return flask.jsonify({"error": str(exc)}), 400
    except Exception:
        return flask.jsonify({"error": "A server error occurred."}), 500


@app.get('/_display')
def display():
    try:
        stored = collection.controls.find_one(
            {"session": flask.session["client_id"]},
            {"_id": 0}  # don't return the document ID
        )
        if stored is not None:
            return stored
        else:
            return flask.jsonify({"No brevet has been saved for this client."}, 400)
    except ValueError as exc:
        return flask.jsonify({"error": str(exc)}), 400
    except Exception:
        return flask.jsonify({"error": "A server error occurred."}), 500

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
