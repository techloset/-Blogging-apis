import pymongo
import certifi
class ConnectionUtil:
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://TestCluster0:TestCluster0@testcluster0.vaeijqh.mongodb.net/?retryWrites=true&w=majority&appName=TestCluster0",tlsCAFile=certifi.where())
        self.db=self.client["Blogs"]
        self.userCollection=self.db["userData"]
        self.postCollection=self.db["postData"]
    def getUserCollection(self):
        return self.userCollection
    def getPostCollection(self):
        return self.postCollection