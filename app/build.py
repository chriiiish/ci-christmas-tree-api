import boto3
import json
import os

#/build/{buildId}/create
def create(event, context):
    build_id = event["pathParameters"]["buildId"]
    send(build_id, 1)
    return response("create", build_id)

#/build/{buildId}/succeed
def succeed(event, context):
    build_id = event["pathParameters"]["buildId"]
    send(build_id, 2)
    return response("succeed", build_id)

#/build/{buildId}/fail
def fail(event, context):
    build_id = event["pathParameters"]["buildId"]
    send(build_id, 3)
    return response("fail", build_id)

#/build/create
def post_create(event, context):
    build_id = get_param(event['body'], "Execution_Id")
    send(build_id, 1)
    return response("create", build_id)

#/build/succeed
def post_succeed(event, context):
    build_id = get_param(event['body'], "Execution_Id")
    send(build_id, 2)
    return response("succeed", build_id)

#/build/fail
def post_fail(event, context):
    build_id = get_param(event['body'], "Execution_Id")
    send(build_id, 3)
    return response("fail", build_id)

#/reset
def reset(event, context):
    send("", 0)
    return response("reset", "")

"""
Sends a message to a topic
build_id = The ID of the build
status = 0 - Reset, 1 - Create, 2 - Success, 3 - Failure
topic = name of topic to send to
"""
def send(build_id, status):
    topic = os.environ['topic']
    client = boto3.client("iot-data")
    payload = json.dumps({
        "buildId": build_id,
        "status": status
    })
    client.publish(
        topic=topic,
        qos=1,
        payload=payload
    )

"""
Generate response
request_type = the type of request sent
build_id = the ID of the build
status = the HTTP status code
"""
def response(request_type, build_id, status=200):
    return{
        "body": json.dumps({
            "type": request_type,
            "id": build_id
        }),
        "statusCode": status
    }

"""
Gets a parameter from a string formatted like so:
key=value&key=value
"""
def get_param(kvpstring, key):
    kvps = kvpstring.split("&")
    keypairs = {}
    for kvp in kvps:
        tkey = kvp.split("=")[0]
        tvalue = kvp.split("=")[1]
        keypairs[tkey] = tvalue
    if key in keypairs:
        return keypairs[key]
    else:
        return None
