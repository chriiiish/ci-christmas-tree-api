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

#/reset
def reset(event, context):
    send("", 0)
    return

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
    return 1

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
