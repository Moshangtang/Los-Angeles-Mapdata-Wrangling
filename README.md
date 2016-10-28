# Los-Angeles-Mapdata-Wrangling
Wrangling the OpenStreetMap data for Los Angeles

OpenStreetMap Sample Project Data Wrangling
with MongoDB
Map Area: Los Angeles, Los Angeles County, California, United States of America
https://www.openstreetmap.org/relation/207359
http://metro.teczno.com/#los-angeles
I live in Los Angeles, so I am very interested in the data from Los Angeles. Hope
to get some new thoughts about the area I live after looking through the map data.
Below is the outline of my report:
1. Problems Encountered in the Map
1.1 Unexpected content for the field of name
1.2 Over-abbreviated street and node names
2. Data Overview
3. Additional Ideas
3.1 Contributer statistics
3.2 Additional data exploration using MongoDB
4. Conclusion
1. Problems Encountered in the Map
After exploring a small sample size of map for Los Angeles area and running it
through data_for_Mongodb.py file, I noticed two main problems which are listed
below. Unlike the sample project, I found all my postal codes (checked over 800)
are correctly formatted and meet my expectation.
1.1 Unexpected content for the field of name.
For example, I expect the node name to be the way like: “Zachary Woods Drive”,
but sometimes, it give me a string like:” Paramount Blvd / MP 10.23”. I split the
string through ‘/’ and deleted the second string for that node by using helper
function “update_name” in data_for_Mongodb.py.
1.2 Over-abbreviated street and node names.
For example, some node name show as “N County Road 2225 E” which I would
like it to be represented as “North County Road 2225 East”. I used helper function
“update_name” in data_for_Mongodb.py.to transform the over-abbreviated names
to be the wanted one.
2. Data Overview
This section contains basic statistics about my Los Angeles dataset and the
MongoDB queries used to gather them.
File sizes
los_angeles.osm ......... 932 MB
los_angeles.osm.json .... 1.20 GB
# Number of documents
>db.mapLA.find().count()
4538513
# Number of nodes
> Query = {"type":"node"}
> db.mapLA.find(Query).count()
4108185
# Number of ways
> Query = {"type":"way"}
> db.mapLA.find(Query).count()
430328
# Number of unique users
> Query = "created.user”
> len(db.mapLA.distinct(Query))
1795
# Top 1 contributing user
>pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
{"$sort":{"count":-1}},
{"$limit":1}]
> db.mapLA.aggregate(pipeline)
{u'count': 619714, u'_id': u'woodpeck_fixbot'}
# Number of users appearing only once (having 1 post)
>pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
{"$group”:{“_id”: “$count”, “num_users”:{“$sum”:1}}},
{“$sort” : {“_id”:1}},
{"$limit":1}]
> db.mapLA.aggregate(pipeline)
{u'num_users': 361, u'_id': 1}
# it means there 361 users who only appear once
3. Additional Ideas
3.1 Contributer statistics
# The top 5 contributors
>pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
{"$sort":{"count":-1}},
{"$limit":1}]
> db.mapLA.aggregate(pipeline)
{u'count': 619714, u'_id': u'woodpeck_fixbot'}
{u'count': 486955, u'_id': u'AM909'}
{u'count': 354784, u'_id': u'vvvexp97'}
{u'count': 332546, u'_id': u'nmixter'}
{u'count': 184964, u'_id': u'Aaron Lidman'}}
There are 4538513 documents in total, top1 contributor contribute about 14% of
them. Top 5 users contribute about 44% which is almost half of the total number.
This indicate the user contribution is skewed, although it is less skewed than that
in sample project.
# Number of users only appear 1,2,3,4 or 5 times
>pipeline = [{"$group":{"_id":"$created.user","count":{"$sum":1}}},
{"$group":{"_id": "$count", "num_users":{"$sum":1}}},
{"$sort" : {"_id":1}},
{"$limit":10}]
>db.mapLA.aggregate(pipeline)
{u'num_users': 361, u'_id': 1}
{u'num_users': 144, u'_id': 2}
{u'num_users': 79, u'_id': 3}
{u'num_users': 57, u'_id': 4}
{u'num_users': 45, u'_id': 5}
Consider the total unique user is 1795, the percentage of contributor that post less
than 6 times to total is 38%. This imply that most of population do not have the
interests in update the data. But I think this is in my expectation since most of the
people only interest in the area they live (like me, I choose Los Angeles as the
database because I live here). So I think the most effective way to get data is to
let more people join in. Although one may contribute only one data, but tons of
people will contribute tons of information.
The strategies I can come up to invite more user to join in is holding on line events
(like gaming) for the contributor as well as their friends who may not be the
contributor. To encourage people to contribute multiple times we should give some
virtual or real rewards for them, like the virtual coins which can be used for some
special titles in this page. And we also can have a page for ranking lists of bestcontributors.
3.2 Additional data exploration using MongoDB
# The postcode shows most times
>pipeline = [{"$match":{"address.postcode":{"$exists":1}}},
{"$group":{"_id":"$address.postcode","count":{"$sum":1}}},
{“$sort” : {“count”:-1}},
{"$limit":1}]
> db.mapLA.aggregate(pipeline)
{u'count': 12396, u'_id': u'92028'}
# Total number of postcodes
> Query = {"address.postcode":{"$exists":1}}
> db.mapLA.find(Query).count()
18821
Together with the result from last query, we can know the appearing ratio of postcode
92028 to total is 12396/18821=0.66, which is quite a lot. The postcode is for Fallbrook,
County of San Diego.
# Top 3 cuisine
>pipeline = ["$match":{"cuisine":{"$exists":1}}},
{"$group":{"_id":"$cuisine","count":{"$sum":1}}},
{"$sort" : {"count":-1}},
{"$limit":3}]
>db.mapLA.aggregate(pipeline)
{u'count': 2, u'_id': u'sandwich'}
{u'count': 2, u'_id': u'burger'}
{u'count': 1, u'_id': u'japanese'}
Unfortunately, there are not too many cuisine styles being denoted.
# Number of amenities
> Query = {"amenity":{"$exists":1}}
> db.mapLA.find(Query).count()
0
I found that, in my Los Angeles map, there is no amenity being denoted.
4. Conclusion
After cleaned and explored my Los Angeles map data base, I found that the data
is incomplete. For example, there are rare cuisine style being denoted and there
are even no data for amenity. However, exploring it was quite fun. I found that the
postcode information of City Fallbrook gives about 66% of total information which
imply that this city has a relative complete address information.
As mentioned in 3.1, the contribution from the user are skewed. The strategies I
can come up to invite more user to join in is holding on line events (like gaming)
for the contributor as well as their friends who may not be the contributor. To
encourage people to contribute multiple times we should give some virtual or real
rewards for them, like the virtual coins which can be used for some special titles in
this page. And we also can have a page for ranking lists of best-contributors. This
can set the best contributor as an example for others.
Also, as we can see from 3.2, relying on user may result information missing (like
cuisine style, amenity). I would like to suggest that this page should have a
programmatically review system to denote the missing information and list on the
page. The user contribute to the missing information can also get some virtual
rewards.
Reference when writing code:
http://stackoverflow.com/tags/r/info
https://docs.mongodb.com/manual/reference/program/mongoimport/
https://discussions.udacity.com/?_ga=1.263919173.837768313.1467659757
