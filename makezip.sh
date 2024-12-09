#!/bin/bash

mkdir package
python3.11 -m pip install --upgrade pip

echo -n "installing developer tools"
 python3 -m pip install awscli-local localstack-sdk-python

echo -n " installing repo"
python3.11 -m pip install --target ./package --use-deprecated=legacy-resolver --no-cache-dir -r requirements-runtime.txt

cd package
zip -r ../currency_exchange_lambda.zip .

cd ..
zip -r currency_exchange_lambda.zip src/
rm -rf package

# create a dynamodb table
echo "\n Configuring the DynamoDB table ..."
awslocal dynamodb create-table \
 --table-name local_currency_exchange \
 --attribute-definitions \
     AttributeName=pk,AttributeType=S \
     AttributeName=sk,AttributeType=S \
 --key-schema \
     AttributeName=pk,KeyType=HASH \
     AttributeName=sk,KeyType=RANGE \
 --provisioned-throughput \
     ReadCapacityUnits=5,WriteCapacityUnits=5 \
 --region us-east-1

# create a AWS Lambda functions
echo "\n Configuring the AWS Lambda Function definition ..."
awslocal lambda create-function \
    --function-name localstack-lambda-currency-exchange \
    --runtime python3.11 \
    --zip-file fileb://currency_exchange_lambda.zip \
    --handler src.worker_lambda.async_lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda_role \
    --tags '{"_custom_id_":"custom-subdomain"}'

# for updating the function-code
# awslocal lambda update-function-code --function-name localstack-lambda-currency-exchange --zip-file fileb://currency_exchange_lambda.zip

# create a SQS FIFO queue
echo "\n Configuring a SQS FIFO queue ..."
 awslocal sqs create-queue --queue-name localstack-currency-exchange
# queue-sqs -> "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/localstack-currency-exchange"

# create event-source-mapping
echo "\n Configuring the AWS EventBridge mapping ..."
awslocal lambda create-event-source-mapping --event-source-arn arn:aws:sqs:us-east-1:000000000000:localstack-currency-exchange --function-name localstack-lambda-currency-exchange --batch-size 1 --enabled --maximum-retry-attempts 2 --starting-position LATEST
#awslocal lambda update-event-source-mapping --uuid b078e68e-b31c-48c7-a128-91c6aaa82339 --batch-size 1

# create the event rule -- cron scheduler [Cloudwatch EventBridge], 5:30 in morning everyday
echo "\n Configuring the Event Rule for Scheduled Cron Job ..."
awslocal events put-rule --name exchange-cron-event --schedule-expression 'cron(30 5 * * ? *)' # arn: "arn:aws:events:us-east-1:000000000000:rule/exchange-cron-event

# now grant event-bridge the permission to invoke lambda
echo "\n Grant permissions to Event-Rule to invoke associated lambda ..."
awslocal lambda add-permission \
--function-name localstack-lambda-currency-exchange \
--statement-id my-scheduled-event \
--action 'lambda:InvokeFunction' \
--principal events.amazonaws.com \
--source-arn arn:aws:events:us-east-1:123456789012:rule/exchange-cron-event

awslocal events put-targets --rule exchange-cron-event --targets file://target.json

# Finally Pulling-up the API-Gateway resources and API Gateway integration services
echo "\n Initializing the API Gateway Resources and API Gateway Integration services ..."
awslocal cloudformation validate-template --template-body file://src/infra/resources.yaml

awslocal cloudformation deploy \
--stack-name lambda-api-gateway \
--template-file src/infra/resources.yaml \
--capabilities CAPABILITY_IAM

echo "Everything done !!"
