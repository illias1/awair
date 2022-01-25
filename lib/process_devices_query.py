
from flask import Flask, jsonify, request

from lib.graphql import graphql
from queries import DEVICES_QUERY


def process_devices_query(param=None, query_type='all'):
    offset = request.args.get('offset')
    variables = {'offset': offset or 0}
    if query_type == 'by_type':
        variables['where'] = {'type': {'_eq': param}}
    elif query_type == 'by_status':
        variables['where'] = {'status': {'_eq': param}}

    try:
        ok, response = graphql(DEVICES_QUERY, variables)
        if ok:
            return jsonify({
                'response': response
            })
        raise Exception
    except Exception as e:
        return jsonify({
            'error': "An exception happened"
        })
