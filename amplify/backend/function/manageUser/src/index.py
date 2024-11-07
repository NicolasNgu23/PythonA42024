import hashlib
import json
import os
import uuid
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

def manageUser(event, context):
    user_table_name = os.environ.get("STORAGE_USERS1_NAME")
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
    table = dynamodb.Table(user_table_name)

    api_key = event['headers'].get('x-api-key')

    if not api_key:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing x-api-key"
            })
        }

    try:

        response = table.scan(
            FilterExpression=Key('id').eq(api_key)
        )

        if response['Items']:
            for item in response['Items']:
                if item.get('id') == api_key:
                    email = item.get('email1')
                    return {
                        "statusCode": 200,
                        "body": json.dumps({
                            "message": "User found",
                            "email": email
                        })
                    }

        user_id = str(uuid.uuid4())
        created_email = f"user_{user_id}@example.com"
        hashCombi = f"{user_id}{created_email}"
        hash_id = hashlib.sha256(hashCombi.encode()).hexdigest()

        new_user = {
            'id': api_key,
            'email1': created_email,
            'hashId': hash_id
        }

        table.put_item(Item=new_user)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "User created successfully",
                "user_id": user_id,
                "email": created_email,
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

    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid input",
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
    return manageUser(event, context)
