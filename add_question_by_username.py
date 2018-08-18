from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import logging
import time
import os
import ast
from random import SystemRandom
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


def add_lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print(" body: ")
    body = ast.literal_eval(event['body'])
    print(body)
    for keys in body:
        print(keys+" - "+body[keys])
    user = body['username']
    question = body['question']
    answer = body['answer']
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')
    print(dynamodb)
    table = dynamodb.Table('question')
    print("check what is the last entry")
    for rand in range(9):
        print(rand)
        user_rand = user+"_"+str(rand)
        print("user count "+user_rand)
        table = dynamodb.Table('questions')
        response = table.query(
            KeyConditionExpression=Key('username').eq(user_rand)
        )
        print("Items: "+str(table.item_count))
        items = response['Items']
        print("Response Items count: "+str(len(items)))
        print(response['Items'])
        for its in items:
            print("single item")
            print(its)
        questions = response['Items']
        print("Questions : ")
        print(questions)
        if str(len(items)) == str(0):
            print("Last unused entry: "+str(rand))
            break
    print("check what is the last entry")
    if(str(rand) > str(3)):
        return {
            'statusCode': 500,
            'body': 'Error - All questions full'
        }    
    else:
        print("add new entry")
        table = dynamodb.Table('questions')
        response = table.put_item(
            Item={
                'username': user_rand,
                'question': question
            }
        )
        table = dynamodb.Table('answers')
        response = table.put_item(
            Item={
                'username': user_rand,
                'answer': answer
            }
        )
        return {
            'statusCode': 200,
            'body': 'OK Question and Answer saved'
        }
    
  