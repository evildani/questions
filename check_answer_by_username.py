from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import logging
import time
import os
from random import SystemRandom
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def lambda_handler(event, context):
    user = event["queryStringParameters"]['username']
    answer = event["queryStringParameters"]['answer']
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    print(dynamodb)
    table = dynamodb.Table('running')
    response = table.query(
        KeyConditionExpression=Key('username').eq(user)
    )
    print("Post runing query")
    items = response['Items']
    print(items)
    for x in items:
        if round(time.time()) < int(x['time']):
            print("check entry in running")
            table = dynamodb.Table('answers')
            user_rand = user+"_"+str(x['id'])
            print("looking for answer for "+user_rand)
            response = table.query(
                KeyConditionExpression=Key('username').eq(user_rand)
            )
            ans = response['Items']
            print(ans)
            for y in ans:
                print("Found answer with id "+str(x['id'])+" here:")
                print(y)
                print(y['answer'])
                if y['answer'] == answer:
                    print ("answer fround, deleting then OK")
                    table = dynamodb.Table('running')
                    response = table.delete_item(
                        Key={
                            'username':  user
                        }
                    )
                    return {
                        'statusCode': 200,
                        'body': 'OK'
                    }
                else:
                    return {
                        'statusCode': 200,
                        'body': 'Wrong Answer'
                    }
        else:
            #no question running, return error.
            print("no question running")
            return {
                        'statusCode': 200,
                        'body': 'No Question Asked'
                    }
            