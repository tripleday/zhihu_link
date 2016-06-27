# encoding=utf-8
import sys

from py2neo import *
from zhihu_crawler import *
from time import sleep
from pymongo import MongoClient

__author__ = 'tripleday'

MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27018
MONGO_DB = 'zhihu'
MONGO_USER_COLL = 'user'
MONGO = MongoClient(MONGO_HOST, MONGO_PORT)

NEO4J_ADDRESS = 'http://localhost:7474/db/data/'
NODE_NAME = 'zhUser'

ZHIHU_COOKIE = ''

GRAPH = Graph(NEO4J_ADDRESS)
CYPHER_FIND_USER = "MATCH (user:" + NODE_NAME + " {%s:'%s'}) RETURN user LIMIT 1"
CYPHER_FIND_RELA = "MATCH (a:{node})-[:FOLLOWING]->(b:{node}) WHERE a._id = '%s' AND b._id = '%s' RETURN a, b".format(node=NODE_NAME)
CYPHER_MIN_PATHS = "MATCH (a:{node} {{ _id:'%s' }}),(b:{node} {{ _id:'%s' }}), p = allShortestPaths((a)-[*..%s]->(b)) RETURN p".format(node=NODE_NAME)

watch("neo4j.http")

GRAPH.delete_all()

# alice = GRAPH.node(25)
# bob = Node("Person", name="Bob", age= 12)
# print alice.properties["age"]
# alice.properties["age"] = 33
# alice.update(age=33)
# print alice.properties["age"]
# bob.properties["age"] = 44
# GRAPH.create(alice)
# GRAPH.create(bob)
# alice_knows_bob = Relationship(alice, "KNOWS", bob)
# GRAPH.create(alice_knows_bob)

# alice.push()
# bob.push()

me = User('https://www.zhihu.com/people/wu-hao-tian-73')
me_item = { '_id':me.data_id, 'name':me.user_id, 'url':me.user_url, 'done':False }
MONGO[MONGO_DB][MONGO_USER_COLL].insert_one(me_item)
me_node = Node("User", name=me_item['name'], _id=me_item['_id'])
GRAPH.create(me_node)

while (True):
    now_item = MONGO[MONGO_DB][MONGO_USER_COLL].find_one({'done': False})
    now_user = User( now_item['url'], now_item['name'], now_item['_id'] )
    now_node = GRAPH.find_one("User", '_id', now_item['_id'])
    # if find_node:
    #     now_node = find_node
    # else:
    #     now_node = Node("User", name=now_item['name'], _id=now_item['_id'])
    #     GRAPH.create(now_node)

    print now_item['name']
    print '**************'

    find_vczh = False
    for e in now_user.get_followers():
        if e.data_id=="0970f947b898ecc0ec035f9126dd4e08":
            find_vczh = True

        if not MONGO[MONGO_DB][MONGO_USER_COLL].find_one({'_id': e.data_id}):
            item = { '_id':e.data_id, 'name':e.user_id, 'url':e.user_url, 'done':False }
            MONGO[MONGO_DB][MONGO_USER_COLL].insert_one(item)

        find_node = GRAPH.find_one("User", '_id', e.data_id)
        if find_node:
            u_node = find_node
        else:
            u_node = Node("User", name=e.user_id, _id=e.data_id)
            # GRAPH.create(now_node)
        rel = Relationship(u_node, "Follow", now_node)
        print e.user_id
        GRAPH.create(rel)

    now_item['done'] = True
    MONGO[MONGO_DB][MONGO_USER_COLL].update_one(
        filter={'_id': now_item['_id']},
        update={'$set': now_item},
        upsert=False
    )

    if find_vczh:
        break

# for rel in GRAPH.match(start_node=alice, rel_type="KNOWS"):
#     print rel.end_node()["name"]