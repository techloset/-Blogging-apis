import pymongo
from app.app_constant import AppConstants
class DatabaseUtil:
    def __init__(self):
        self.userCollection=AppConstants.db.getUserCollection()
        self.postCollection=AppConstants.db.getPostCollection()

        
    '''
    .////////  User collection ////////
    '''
    def findOneUser(self,findQuery):
       return self.userCollection.find_one(findQuery)
    def insertOneUser(self,insertQuery):
        self.userCollection.insert_one(insertQuery) 
    def deleteOneUser(self,deleteQuery):
        self.userCollection.delete_one(deleteQuery)     
    def updateOneUser(self,findQuery,updateQuery):
        self.userCollection.update_one(findQuery,updateQuery)          
    '''
    ///////    Post Collection //////////
    '''
    def findOnePost(self,findQuery):
       return self.postCollection.find_one(findQuery)
    def findPost(self, findQuery, limit=None):
        if limit is None:
            return list(self.postCollection.find(findQuery))
        else:
            return list(self.postCollection.find(findQuery).limit(limit))
        
    def insertOnePost(self,insertQuery):
        self.postCollection.insert_one(insertQuery)  

    def updateOnePost(self,findQuery,updateQuery):
        self.postCollection.update_one(findQuery,updateQuery)
    def deleteOnePost(self,deleteQuery):
        self.postCollection.delete_one(deleteQuery) 
    def deleteManyPost(self,deleteQuery):
        self.postCollection.delete_many(deleteQuery)        
    def createOnePostIndex(self):
        self.postCollection.create_index([("title", pymongo.TEXT)])            