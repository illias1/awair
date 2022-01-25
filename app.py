# app.py
import logging

from flask import Flask, jsonify
from lib.graphql import graphql
from lib.process_devices_query import process_devices_query

from queries import DEVICE_BY_ID_QUERY, DEVICES_QUERY

import logging
log = logging.getLogger(__name__)

app = Flask(__name__)



@app.route("/device/<string:device_id>")
def get_device_by_id(device_id):
    variables = {'id': device_id}
    try:
        ok, response = graphql(DEVICE_BY_ID_QUERY, variables)
        if ok:
            return jsonify({
                'response': response
            })
        raise Exception
    except Exception as e:
        return jsonify({
            'error': "An exception happened"
        })


@app.route("/devices")
def get_devices():
    return process_devices_query()


@app.route("/devices/type/<string:device_type>")
def get_devices_by_type(device_type):
    return process_devices_query(param=device_type, query_type="by_type")


@app.route("/devices/status/<string:device_status>")
def get_devices_by_status(device_status):
    return process_devices_query(param=device_status, query_type="by_status")
