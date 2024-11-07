from distutils.core import setup

setup(name='src', version='1.0')
# import json
# import os
# import boto3
# from botocore.exceptions import ClientError

# def getToken(event, context):
#     print('received event:')
#     print(event)

#     user_table_name = os.environ.get("STORAGE_USERS1_NAME")
#     dynamodb = boto3.resource('dynamodb', region_name="eu-west-1")
#     table = dynamodb.Table(user_table_name)

#     email = event['headers'].get('x-api-key')

#     if not email:
#         pass
#     res = table.query


# def createUser(event, context):
#     print('creating user')
#     print(event)
#     user_table_name = os.environ.get("STORAGE_USERS1_NAME")
#     dybamodb = boto3. resource('dynamodb', region_name="eu-west-1")
#     table = dynamodb.Table(user_table_name)


#     user_id = event['headers'.get('userId')]

#     if not user_id
#         pass
#     res =
