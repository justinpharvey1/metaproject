from __future__ import print_function

import boto3
import json

import mysql.connector

print('Loading function')


def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - commenttext: text of the new comment
      - parentcoment: the parent comment ID (0 if comment is top level under post)
      - parentpost: parent post ID
    '''
    #print("Received event: " + json.dumps(event, indent=2))


    commenttext = event['commenttext']
    parentcomment = event['parentcomment']
    parentpost = event['parentpost']


    print("checkpoint1")


    cnx = mysql.connector.connect(user='masterusername', password='masterpassword', host=' mydbinstance.cctousqbj3wu.us-east-1.rds.amazonaws.com', database='records')
    cursor = cnx.cursor()

    query = ("INSERT INTO comments (commenttext, parentpost, parentcomment) VALUES (" + "'" + commenttext + "','" + parentpost + "','" +  parentcomment + "');")
    cursor.execute(query)
   
    cnx.commit()

    cursor.close()
    cnx.close()








    return("hello world")