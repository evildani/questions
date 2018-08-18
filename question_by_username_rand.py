from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import logging
import time
from random import SystemRandom
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def handler (event, context):

    onTheFly = False
    cryptogen = SystemRandom()
    rand = cryptogen.randrange(3) #remove 0
    user = event["queryStringParameters"]['username']
    print("Received query for user= "+user)
    user_rand = user+"_"+str(rand)
    print("Converted query for user_rand= "+user_rand)
    
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    print(dynamodb)
    table = dynamodb.Table('running')
    response = table.query(
        KeyConditionExpression=Key('username').eq(user)
    )
    print("Is there a running entrey")
    items = response['Items']
    print("items for running ")
    print(items)
    for x in items:
        if x['username'] == user:
            print("question on the fly already, sending same question")
            rand = x['id']
            onTheFly = True
            user_rand = user+"_"+str(rand)
            print("updated time on running to: "+str(round(time.time()+180)))
    print("here is the question: ")
    table = dynamodb.Table('questions')
    print("Items: "+str(table.item_count))
    response = table.query(
        KeyConditionExpression=Key('username').eq(user_rand)
    )
    items = response['Items']
    ##store username in table running to check answer later.
    table = dynamodb.Table('running')
    response = table.put_item(
        Item={
            'username': user,
            'id':rand,
            'time': str(round(time.time()+180))
        }
    )
    print("return: ")
    for x in items:
        print(x['question'])
        return {
            'statusCode': 200,
            'body': x['question']
        }