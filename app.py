# app.py
from lib.upload_process_devices import process_devices_json_file_upload
from queries import DEVICE_BY_ID_QUERY
import logging

from flask import Flask, jsonify

from lib.graphql import graphql
from lib.general_devices_query import general_devices_query


log = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/device/<string:device_id>")
def get_device_by_id(device_id):
    variables = {'id': device_id}
    try:
        response = graphql(DEVICE_BY_ID_QUERY, variables)
        return jsonify({
            'response': response
        })
    except Exception as e:
        return jsonify({
            'error': "An exception happened: %" %e
        })


@app.route("/devices")
def get_devices():
    return general_devices_query()


@app.route("/devices/type/<string:device_type>")
def get_devices_by_type(device_type):
    return general_devices_query(param=device_type, query_type="by_type")


@app.route("/devices/status/<string:device_status>")
def get_devices_by_status(device_status):
    return general_devices_query(param=device_status, query_type="by_status")


@app.route("/upload_devices", methods=["POST"])
def upload_devices():
    process_devices_json_file_upload()
    return "ok"
