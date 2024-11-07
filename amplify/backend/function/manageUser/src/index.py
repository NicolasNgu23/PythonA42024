import hashlib
import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def handler(event, context):
    user_table_name = os.environ.get("STORAGE_USERS1_NAME")
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
    table = dynamodb.Table(user_table_name)

    user_id = event['headers'].get('x-api-key')

    if user_id:
        try:
            res = table.query(
                IndexName='emails1',
                KeyConditionExpression=Key('email1').eq(user_id)
            )

            if 'Items' in res and res['Items']:
                existing_user = res['Items'][0]
                print(existing_user)
                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "User found",
                        "email": existing_user['email1']
                    })
                }
            else:
                return {
                    "statusCode": 404,
                    "body": json.dumps({
                        "error": "User not found"
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
    else:
        new_user_id = str(uuid.uuid4())
        created_email = f"user_{new_user_id}@example.com"
        hashCombi = f"{new_user_id}{created_email}"
        hash_id = hashlib.sha256(hashCombi.encode()).hexdigest()

        new_user = {
            'id': new_user_id,
            'email1': created_email,
            'hashId': hash_id
        }

        try:
            table.put_item(Item=new_user)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "User created successfully",
                    "user": new_user
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
