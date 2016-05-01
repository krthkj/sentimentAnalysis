import pymongo
import csv
import os

conn = pymongo.MongoClient()
tweetdb=conn.twitter_db.tweets_1
#cursor = tweetdb.find({},{'_id':0,'id':'','text':'','location':'','age':'','sentiment':'','score':'','retweet_count':'','user.friends_count':'','user.followers_count':'','user.screen_name':'','user.favourites_count':''})
cursor = tweetdb.find({},{'_id':0,'id':'','location':'','age':'','sentiment':'','score':'','user.followers_count':''})
#cursor = tweetdb.find({},{'_id':0,'id':'','location':'','age':'','sentiment':'','score':''})

#
with open('asdxk.csv', 'w') as outfile:
    #fields = ['id','text','location','age','sentiment','score','retweet_count','user.friends_count','user.followers_count','user.screen_name','user.favourites_count']
    #fields = ['id','location',"age",'sentiment','score','followers_count']
    fields = ['id','location',"age",'sentiment','score',['followers_count']]
    writer = csv.DictWriter(outfile, fieldnames=fields)
    writer.writeheader()
    for x in cursor:
        writer.writerow(x)

