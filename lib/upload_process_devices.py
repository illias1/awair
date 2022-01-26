import json
import logging
from urllib.request import urlopen
import ijson
from lib.graphql import graphql
from queries import DEVICES_UPSERT_MUTATION


log = logging.getLogger(__name__)

BATCH_SIZE = 50


def process_devices_json_file_upload():
    streamed_devices = {}

    # Since we have limited memory:
    # processing the file as a stream and process devices by small batches
    parser = ijson.parse(urlopen(
        'https://menu-item-images10723-new.s3.ap-northeast-2.amazonaws.com/awair/devices.json'))
    for prefix, _, value in parser:
        id = ''
        if (
            prefix.endswith('.id') or
            prefix.endswith('.status') or
            prefix.endswith('.timezone') or
            prefix.endswith('.type')
        ):
            id, key = prefix.split('.')
            check_if_new_id_and_process_previous_batch(id, streamed_devices)
            streamed_devices[id][key] = value
        elif prefix.endswith('.coordinates.item'):
            id, _, _ = prefix.split('.')
            check_if_new_id_and_process_previous_batch(id, streamed_devices)
            if 'coordinates' not in streamed_devices[id]:
                streamed_devices[id]['coordinates'] = []
            streamed_devices[id]['coordinates'].append(float(value))

    # process last ones at the end of the file
    process_devices_batch(streamed_devices)


# If id isn't in the dict yet,
# means just finished adding previous item to the dictionary
# and may need to process previous batch
def check_if_new_id_and_process_previous_batch(id, devices_dict):
    if id not in devices_dict:
        if len(devices_dict) >= BATCH_SIZE:
            process_devices_batch(devices_dict)
            devices_dict.clear()
        devices_dict[id] = {}


# Check devices' integrity and save them to the db
def process_devices_batch(devices_dict):
    are_all_devices_complete = check_devices_integrity(devices_dict)
    if not are_all_devices_complete:
        log.error('Some devices don\'t have all properties')
        log.error(json.dumps(devices_dict, indent=2))
        # + specify which ones
        return

    # on_conflict ensures that the item is updated if id already exists in db
    variables = {
        "objects": [value for _, value in devices_dict.items()],
        "on_conflict": {"constraint": "devices_pkey", "update_columns": ["status", "type", "timezone", "coordinates"]}
    }
    try:
        response = graphql(DEVICES_UPSERT_MUTATION, variables)
    except Exception as e:
        log.error('Exception happened at graphql request')
        log.error(e)
        # + log whatever details needed


# Check all expected properties are present in each device dict and
# that there are 2 or 0 coordinates (if the case of c44dt2ecie6h7m4lihdg is normal)
def check_devices_integrity(devices_dict):
    DEVICE_KEYS = ['id', 'status', 'timezone', 'type']
    for device_key in devices_dict:
        for key in DEVICE_KEYS:
            if key not in devices_dict[device_key]:
                return False
        if (
            'coordinates' in devices_dict[device_key] and
            (len(devices_dict[device_key]['coordinates']) not in [0, 2])
        ):
            return False
    return True


# Since the solution is designed as a serverless function and they usually have a time limit
# the draft below would be a workaround around the big size file problem
# Once the time limit is approaching - invoke the same function with advanced line offset
# Since I'm already behind the time schedule and this could be reused in a static server - not implementing


# def invoke_lambda(function_name, event):
#     payload = json.dumps(event).encode('utf-8')
#     client = boto3.client('lambda')
#     response = client.invoke(
#         FunctionName=function_name,
#         InvocationType='Event',
#         Payload=payload
#     )


# # process and do work
# if context.get_remaining_time_in_millis() < MINIMUN_REMAINING_TIME_MS:
#     break

# new_offset = offset + previous_offset
# if new_offset < s3_object.content_length:
#     new_event = {
#         **event,
#         "offset": new_offset,
#     }
#     invoke_lambda(context.function_name, new_event)
# return
