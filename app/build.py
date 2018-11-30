import boto3
import json

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

# Called by a separate event to reset the state of the tree
def reset(event, context):
    send("", 0)
    return

"""
Sends a message to a topic
build_id = The ID of the build
status = 1 - Create, 2 - Success, 3 - Failure
topic = name of topic to send to
"""
def send(build_id, status, topic="buildmasterchristmastree"):
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