from __future__ import print_function

import boto3
import json

import mysql.connector

print('Loading function')


def lambda_handler(event, context):
    '''Provide an event that contains the following keys:

      - mediatype: comment or post 
      - mediaid: postid or commentid
      - change: upvote or downvote (-1 or +1)
    '''
    #print("Received event: " + json.dumps(event, indent=2))


    mediaID = event['id']



    if (str(event['type']) == "comment"): 
        mediatype = "comments"

    if (str(event['type']) == "post"):
        mediatype = "posts"



    change = event['change']



    print("checkpoint1")


    cnx = mysql.connector.connect(user='masterusername', password='masterpassword', host=' mydbinstance.cctousqbj3wu.us-east-1.rds.amazonaws.com', database='records')
    cursor = cnx.cursor()




    #update score
    if (str(mediatype) == "comments"):
        #update vote count
        query = ("UPDATE " + str(mediatype) + " SET votes = votes + 1 WHERE commentID = " + mediaID + ";")
        cursor.execute(query)
        cnx.commit()

        if (int(change) == 1):
            query = ("UPDATE " + str(mediatype) + " set score = score +  1 WHERE commentID = " + mediaID + ";")
        else: 
            query = ("UPDATE " + str(mediatype) + " set score = score -  1 WHERE commentID = " + mediaID + ";")




    if (str(mediatype) == "posts"):
        #update vote count
        query = ("UPDATE " + str(mediatype) + " SET votes = votes + 1 WHERE postID = " + mediaID + ";")
        cursor.execute(query)
        cnx.commit()
        if (int(change) == 1):
            query = ("UPDATE " + str(mediatype) + " set score = score +  1 WHERE postID = " + mediaID + ";")
        else: 
            query = ("UPDATE " + str(mediatype) + " set score = score -  1 WHERE postID = " + mediaID + ";")



    cursor.execute(query)
    cnx.commit()




    cursor.close()
    cnx.close()






    return("hello world")