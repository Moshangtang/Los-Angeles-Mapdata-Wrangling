from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.mydb

num_total = db.mapLA.find().count()
print 'The number of documents is: ', num_total

Query = {'type':'node'}
num_nodes = db.mapLA.find(Query).count()
print 'The number of nodes is: ', num_nodes

Query = {'type':'way'}
num_ways = db.mapLA.find(Query).count()
print 'The number of ways is: ', num_ways

Query = {"created.user"}
list_unique_user = db.mapLA.distinct("created.user")
num_unique_user = len(list_unique_user)
print 'The number of unique users is: ', num_unique_user

# Top 1 contributing user
pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit":1}]
cursor = db.mapLA.aggregate(pipeline)
for i in cursor:
    print(i)

#Number of users appearing only once (having 1 post)
pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
            {"$group":{"_id": "$count", "num_users":{"$sum":1}}},
            {"$sort" : {"_id":1}},
            {"$limit":1}]

cursor = db.mapLA.aggregate(pipeline)
for i in cursor:
    print(i)

#The postcode shows most times
pipeline = [{"$match":{"address.postcode":{"$exists":1}}},
            {"$group":{"_id":"$address.postcode","count":{"$sum":1}}},
            {"$sort" : {"count":-1}},
            {"$limit":1}]

cursor = db.mapLA.aggregate(pipeline)
for i in cursor:
    print(i)

# Top 3 cuisine

pipeline = [{"$match":{"cuisine":{"$exists":1}}},
            {"$group":{"_id":"$cuisine","count":{"$sum":1}}},
            {"$sort" : {"count":-1}},
            {"$limit":3}]
cursor = db.mapLA.aggregate(pipeline)
for i in cursor:
    print(i)

Query = {"address.postcode":{"$exists":1}}
num_postcode = db.mapLA.find(Query).count()
print 'The number of postcode is: ', num_postcode


pipeline = [{"$match":{"amenity":{"$exists":1}}},
            {"$group":{"_id":"$amenity","count":{"$sum":1}}},
            {"$sort" : {"count":-1}},
            {"$limit":5}]
cursor = db.mapLA.aggregate(pipeline)
for i in cursor:
    print(i)

Query = {"amenity":{"$exists":1}}
num_amenity = db.mapLA.find(Query).count()
print 'The number of amenity is: ', num_amenity

# Top 5 contributing users
pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
            {"$sort":{"count":-1}},
            {"$limit":5}]
cursor = db.mapLA.aggregate(pipeline)
for i in cursor:
    print(i)
