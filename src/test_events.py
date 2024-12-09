import datetime
import uuid

api_currency_exchange_event = {
    "resource": "/api/v1/kaizen/fetch-currency-exchange/{proxy+}",
    "path": "/api/v1/kaizen/fetch-currency-exchange/generate",
    "httpMethod": "GET",
    "headers": {
        "Host": "localhost",
        "Postman-Token": "2ca302ec-8cd5-45cc-8493-b4dabdfdea65",
        "X-Amzn-Trace-Id": "Root=1-63fd73f9-326f10814a3f34a10ce96b1b",
        "x-api-key": "ZzU4CwLskqa40Hv1f2vLP21uGyUc5lLF5cEhLe2M",
        "X-Forwarded-For": "27.116.40.158",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https",
    },
    "multiValueHeaders": {
        "Host": ["localhost"],
        "Postman-Token": ["2ca302ec-8cd5-45cc-8493-b4dabdfdea65"],
        "X-Amzn-Trace-Id": ["Root=1-63fd73f9-326f10814a3f34a10ce96b1b"],
        "x-api-key": ["ZzU4CwLskqa40Hv1f2vLP21uGyUc5lLF5cEhLe2M"],
        "X-Forwarded-For": ["27.116.40.158"],
        "X-Forwarded-Port": ["443"],
        "X-Forwarded-Proto": ["https"],
    },
    "queryStringParameters": {"":""
        # "date-param": f"{datetime.datetime.now().date()}",
        },
    "multiValueQueryStringParameters": None,
    "pathParameters": {"proxy": "docs/12345/status"},
    "stageVariables": {"lambdaAlias": "dev"},
    "requestContext": {
        "resourceId": "9bfmqc",
        "resourcePath": "/api/v1/nirvana/loss-run/{proxy+}",
        "httpMethod": "GET",
        "extendedRequestId": "BB8O-HhxBcwFmXg=",
        "requestTime": "28/Feb/2023:03:24:41 +0000",
        "path": "/dev/api/v1/kaizen/currency-exchange/generate",
        "accountId": "000000000000",
        "protocol": "HTTP/1.1",
        "stage": "dev",
        "domainPrefix": "api",
        "requestTimeEpoch": 1677554681138,
        "requestId": "44e5ffda-8b28-4e22-bb57-fdf8716ca9a0",
        "identity": {
            "cognitoIdentityPoolId": None,
            "cognitoIdentityId": None,
            "apiKey": "ZzU4CwLskqa40Hv1f2vLP21uGyUc5lLF5cEhLe2M",
            "principalOrgId": None,
            "cognitoAuthenticationType": None,
            "userArn": None,
            "apiKeyId": "65w3zyn54m",
            "userAgent": None,
            "accountId": None,
            "caller": None,
            "sourceIp": "27.116.40.158",
            "accessKey": None,
            "cognitoAuthenticationProvider": None,
            "user": None,
        },
        "domainName": "localhost",
        "apiId": "z793za7cl9",
    },
    "body": None,
    "isBase64Encoded": False,
}


report_generation_cron_event = {
    "version": "0",
    "id": "a8e7d541-e307-fa2c-565b-49ec5f7adbe6",
    "detail-type": "Scheduled Event",
    "source": "aws.events",
    "account": "748276930737",
    "time": "2023-03-10T08:25:00Z",
    "region": "ap-south-1",
    "resources": [
        "arn:aws:events:ap-south-1:0000000000:rule/dev-kaizen-currency-scheduled-rule"
    ],
    "detail": {},
}