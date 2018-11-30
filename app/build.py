import boto3
import json

#/createbuild/{buildId}
def create(event, context):
    send(event["pathParameters"]["buildId"], 1)
    return{ "statusCode": 200 }

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