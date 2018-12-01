# ci-christmas-tree-api
The Online API that the build system hooks into to publish to the raspberry pi

# Deployment
To build the application:

```bash
sam package --template-file template.yml --s3-bucket <YOUR S3 BUCKET> --output-template-file packaged.yaml
```
To deploy the application

```bash
sam deploy --template-file packaged.yaml --stack-name <MY STACK NAME> --capabilities CAPABILITY_NAMED_IAM
# Or to Deploy with a particular topic:
# sam deploy --template-file packaged.yaml --stack-name <MY STACK NAME> --parameter-overrides "topic=<mytopic>" --capabilities CAPABILITY_NAMED_IAM
```

# IoT Policy
You can run the `iot-policy.cfn.yaml` template to create the policy for the IoT devices
