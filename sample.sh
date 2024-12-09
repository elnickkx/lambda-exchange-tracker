#!/bin/bash

# AWS CLI commands on validate APIGateway integration on localstack Cloud emulator
# creating the APIgateway resources and integration with existing lambda
#awslocal apigateway create-rest-api --name 'API Gateway Lambda integration'
#"""
#{
#    "id": "gnbeudkfue", # rest-api-id -- child API key, unique throughout API-Gateway
#    "name": "API Gateway Lambda integration",
#    "createdDate": 1733703295.0,
#    "apiKeySource": "HEADER",
#    "endpointConfiguration": {
#        "types": [
#            "EDGE"
#        ]
#    },
#    "disableExecuteApiEndpoint": false,
#    "rootResourceId": "eyml83s8ls"
#}
#"""
#
#awslocal apigateway get-resources --rest-api-id gnbeudkfue
#"""
#{
#    "items": [
#        {
#            "id": "eyml83s8ls",
#            "path": "/"
#        }
#    ]
#}
#
#"""
#awslocal apigateway create-resource \
#  --rest-api-id gnbeudkfue \
#  --parent-id eyml83s8ls \
#  --path-part "api"
#"""
#{
#    "id": "hzrwd2i3ln",
#    "parentId": "eyml83s8ls",
#    "pathPart": "api",
#    "path": "/api"
#}
#"""
#
#awslocal apigateway put-method \
#  --rest-api-id gnbeudkfue \
#  --resource-id hzrwd2i3ln \
#  --http-method GET \
#  --request-parameters "method.request.path.api=true" \
#  --authorization-type "NONE"
#
## APIGateway integration method
#awslocal apigateway put-integration \
#  --rest-api-id gnbeudkfue \
#  --resource-id hzrwd2i3ln \
#  --http-method GET \
#  --type AWS_PROXY \
#  --integration-http-method GET \
#  --uri arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:localstack-lambda-currency-exchange/invocations \
#  --passthrough-behavior WHEN_NO_MATCH
#
## create the APIGATEWAY deployment
#awslocal apigateway create-deployment \
#  --rest-api-id gnbeudkfue \
#  --stage-name dev