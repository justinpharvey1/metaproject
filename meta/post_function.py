from __future__ import print_function

from math import hypot
from decimal import *

import boto3
import json

import datetime
import mysql.connector


def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - geocode: location of the request (required)
      - text: the text query to search with
      - image: image URL pointing to S3 object
    '''
    
    #print("Received event: " + json.dumps(event, indent=2))


    querylatitude = event['latitude']
    querylongitude = event['longitude']
    text = event['text']
    image = event['imageurl'] 

    
    
    print("checkpoint1")

    cnx = mysql.connector.connect(user='masterusername', password='masterpassword', host=' mydbinstance.cctousqbj3wu.us-east-1.rds.amazonaws.com', database='records')
    cursor = cnx.cursor()

    query = ("INSERT INTO posts (postname, latitude, longitude) VALUES (" + "'" + text + "','" + querylatitude + "','" +  querylongitude + "');")
    cursor.execute(query)
   
    cnx.commit()

    cursor.close()
    cnx.close()

    return("hello world")
    
   

   