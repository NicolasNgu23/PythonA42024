import hashlib
import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def getToken(event, context):
    user_table_name = os.environ.get("STORAGE_USERS1_NAME")
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
    table = dynamodb.Table(user_table_name)

    email = event['headers'].get('email')
    if not email:
        return {
            "statusCode": 400,
            "body": "Missing email!"
        }

    try:

        print(email)
        res = table.query(
            IndexName='emails1',
            KeyConditionExpression=Key('email1').eq(email)
        )
        print(res)
        if res['Items']:
            user_id = res['Items'][0].get('id')
            hash_value = res['Items'][0].get('hashId')
            print("User already exists")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "user_id": user_id,
                    "email": email,
                    "hash_value": hash_value
                })
            }
        else:
            user_id = str(uuid.uuid4())
            hashCombi = f"{user_id}{email}"
            hash_id = hashlib.sha256(hashCombi.encode()).hexdigest()

            new_user = {
                'id': user_id,
                'email1': email,
                'hashId': hash_id
            }

            table.put_item(Item=new_user)
            print("New user created")

            return {
                "statusCode": 201,
                "body": json.dumps({
                    "message": "User created successfully",
                    "email": email,
                    "hashId": hash_id
                })
            }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "DynamoDB ClientError",
                "message": str(e)
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Unexpected error",
                "message": str(e)
            })
        }

def handler(event, context):
    return getToken(event, context)
