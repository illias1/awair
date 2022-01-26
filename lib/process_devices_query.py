
from flask import Flask, jsonify, request

from lib.graphql import graphql
from queries import DEVICES_QUERY


def process_devices_query(param=None, query_type='all'):
    offset = request.args.get('offset')
    limit = request.args.get('limit')
    variables = {
        'offset': int(offset) if offset else 0,
        'limit': int(limit) if limit else 100
    }
    if query_type == 'by_type':
        variables['where'] = {'type': {'_eq': param}}
    elif query_type == 'by_status':
        variables['where'] = {'status': {'_eq': param}}

    try:
        response = graphql(DEVICES_QUERY, variables)
        return jsonify({
            'response': response
        })
    except Exception as e:
        return jsonify({
            'error': "An exception happened"
        })
