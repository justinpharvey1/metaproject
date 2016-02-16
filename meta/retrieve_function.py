#The flow of this module is to first query by location. Then, take the nearby posts and filter them by image/text if applicable


from __future__ import print_function

from math import hypot
from decimal import *

import boto3
import json

import datetime
import mysql.connector





def build_comments(postID):

    connection = mysql.connector.connect(user='masterusername', password='masterpassword', host=' mydbinstance.cctousqbj3wu.us-east-1.rds.amazonaws.com', database='records')
    
    query = ("SELECT commentID, commenttext, votes, score, depth, parentpost, parentcomment from comments WHERE parentpost = " + "'" + str(postID) + "';")

    cursor = connection.cursor()
    cursor.execute(query)

    commentlist = []

    for (commentID, commenttext, votes, score, depth, parentpost, parentcomment) in cursor:
   


        commentdictionary = {}
        commentdictionary['parentpost'] = str(parentpost)
        commentdictionary['parentcomment'] = str(parentcomment)
        commentdictionary['commentID'] = str(commentID)
        commentdictionary['commenttext'] = str(commenttext)
        commentdictionary['votes'] = str(votes)
        commentdictionary['score'] = str(score)
        commentdictionary['depth'] = str(depth)

        commentlist.append(commentdictionary)


    return(commentlist)





def compute_text_similarity(query, titletext, bodytext): 

    print ("hello world")





def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - geocode: location of the request (required)
      - text: the text query to search with
      - image: image URL pointing to S3 object
    '''
    
    #print("Received event: " + json.dumps(event, indent=2))


    SEARCH_RADIUS = .005


    #parse url parameters
    querylatitude = event['latitude']
    querylongitude = event['longitude']
    text = event['text']
    image = event['imageurl'] 
    

    #connect to database
    cnx = mysql.connector.connect(user='masterusername', password='masterpassword', host=' mydbinstance.cctousqbj3wu.us-east-1.rds.amazonaws.com', database='records')





    responseList = []

   
    #query database for posts
    query = ("SELECT postID, postname, posttext, images, latitude, longitude, votes, score, wiki FROM posts")
    cursor = cnx.cursor()
    cursor.execute(query)

    #loop through post results
    
    flag = 0
    for (postID, postname, posttext, images, latitude, longitude, votes, score, wiki) in cursor:
      distance = hypot(Decimal(querylatitude)-Decimal(latitude), Decimal(querylongitude)-Decimal(longitude))

      #If distance less than search radius, add result to results string
      if (distance <= SEARCH_RADIUS): 
        flag = 1
        print ("Found Match: ", distance)

     

        #Add Data to response dictionary
        dictionary = {}
        dictionary['postID'] = str(postID)
        dictionary['postname'] = str(postname)
        dictionary['posttext'] = str(posttext)
        dictionary['imageurls'] = str(images)
        dictionary['latitude'] = str(latitude)
        dictionary['longitude'] = str(longitude)
        dictionary['votes'] = str(votes)
        dictionary['score'] = str(score)
        dictionary['wiki'] = str(wiki)


        #build comments
        commentlist = build_comments(postID)
        dictionary['comments'] = commentlist



        responseList.append(dictionary)


    cursor.close()


   
    #posts = {'postID':1,'postname':'sampleName','posttext':'sampleText','imageurls':None,'latitude':30.2844,'longitude':-97.7194,'votes':3,'score':1,'wiki':0}
    #responseList.append(posts)


    cnx.close()

    
    print("Query Latitude: ", querylatitude)
    print("Query Longitude: ", querylongitude)
    print("Query Text: ", text)
    print("Query Image: ", image)



    return(responseList)





   