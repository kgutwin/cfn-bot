#!/bin/bash

set -e

STACK_NAME=cfn-bot
S3_BUCKET=$(aws s3 ls | awk '/sam-deployments/{print $NF}')
if [[ -z $S3_BUCKET ]]; then
    S3_BUCKET=sam-deployments-$RANDOM$RANDOM
    aws s3 mb s3://$S3_BUCKET
fi

# load twitter keys
. ./.twitter_keys

make build SERVICE=cfnbot

sam package --template-file template.yaml \
    --output-template-file serverless-output.yaml \
    --s3-bucket $S3_BUCKET

sam deploy --region us-east-1 \
    --template-file serverless-output.yaml \
    --stack-name $STACK_NAME \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides "TwitterAccessTokenKey=$TWITTER_ACCESS_TOKEN_KEY" \
    "TwitterAccessTokenSecret=$TWITTER_ACCESS_TOKEN_SECRET"

