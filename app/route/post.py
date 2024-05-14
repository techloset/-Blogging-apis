from fastapi import APIRouter,Depends,status,HTTPException,Body,HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from app.models import AddPostModel,Comment,CommentUniquId
from app.utils import DatabaseUtil,JwtHelper
from app.app_constant import AppConstants
route=APIRouter()
dbUtil=DatabaseUtil()
@route.get("/")
def test():
    return {"Hello":"Post"}
# Route to add a new post
@route.post("/addPost")
def addPost(credentials: HTTPAuthorizationCredentials = AppConstants.jwt_auth(),
            postInfo: AddPostModel = Body(..., title="Add post")):
    """
    Add a new post to the blog.

    Parameters:
    - credentials (HTTPAuthorizationCredentials): User credentials for authentication.
    - postInfo (AddPostModel): Information of the post to be added.

    Returns:
    - dict: A dictionary containing a success message and details of the newly added post.
    """
    try:
        postId = AppConstants.uniqueid()
        userInfo = dbUtil.findOneUser({"_id": credentials})
        postData = {
            "_id": postId,
            "dateTime": AppConstants.currentDateTime(),
            "title": postInfo.title,
            "content": postInfo.content,
            "category": postInfo.category,
            "tags": postInfo.tags,
            "comment": postInfo.comment,
            "like": postInfo.like,
            "userId": userInfo["_id"],
            "author": userInfo["firstName"] + " " + userInfo["lastName"],
        }
        dbUtil.insertOnePost(postData)
        return {"message": "Post uploaded successfully", "newPost": postData}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

# Route to get all posts
@route.get("/getAllPost/{limit}")
def getAllPosts(limit: int, credentials: HTTPAuthorizationCredentials = AppConstants.jwt_auth()):
    """
    Get all posts.

    Parameters:
    - limit (int): Maximum number of posts to retrieve.
    - credentials (HTTPAuthorizationCredentials): User credentials for authentication.

    Returns:
    - dict: A dictionary containing details of all the retrieved posts.
    """
    try:
        allPosts = dbUtil.findPost({}, limit=limit)       
        if len(allPosts) == 0:
            return {"message": "No posts found"}
        return {"message": "Posts retrieved successfully", "allPosts": allPosts}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

# Route to get a single post by postId
@route.get("/singlePost/{postId}")
def getSinglePost(postId: str, credentials: HTTPAuthorizationCredentials = AppConstants.jwt_auth()):
    """
    Get a single post by its postId.

    Parameters:
    - postId (str): Identifier of the post to retrieve.
    - credentials (HTTPAuthorizationCredentials): User credentials for authentication.

    Returns:
    - dict: A dictionary containing details of the retrieved post.
    """
    try:
        singlePost = dbUtil.findOnePost({"_id": postId})
        if singlePost is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return singlePost
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e

@route.delete("/deletePost/{postId}")
def deletePost(postId:str,cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
        dbUtil.deleteOnePost({"_id":postId})
        return {"message":"Post successfully Deleted"}
    except Exception as e:
        return{"message":f"Internal server error {e}"}
    
@route.put("/updatePost/{postId}")
def updatePost(postId:str,postInfo:AddPostModel=Body(...,title="Update post"),cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
        updateQuery={"$set":{
           "title": postInfo.title,
            "content": postInfo.content,
            "category": postInfo.category,
            "tags": postInfo.tags,
        }
        }
        dbUtil.updateOnePost({"_id":postId},updateQuery)
    except Exception as e:
        return {"message":f"Internal server error{e}"}    

@route.get("/searchPost/{search_query}")
def searchPost(search_query:str,cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
      dbUtil.createOnePostIndex()
      matchingPosts=dbUtil.findPost({"$text":{"$search":search_query}})
      return {"message":"Search successfully","allPosts":matchingPosts} 
    except Exception as e:
        return{"message":f"Internal server error {e}"}   
# Route to get specific user posts
@route.get("/specificUserPosts/{limit}")
def getSpecificUserPost(limit: int, credentials: HTTPAuthorizationCredentials = AppConstants.jwt_auth()):
    """
    Get posts of a specific user.

    Parameters:
    - limit (int): Maximum number of posts to retrieve.
    - credentials (HTTPAuthorizationCredentials): User credentials for authentication.

    Returns:
    - dict: A dictionary containing details of the specific user posts.
    """
    try:
       
        specificUserPost = dbUtil.findPost({"userId": credentials}, limit=limit)
        if len(specificUserPost) == 0:
            return {"message": "No posts found for the specified user"}
        return {"message": "User posts retrieved successfully", "specificUserPost": specificUserPost}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error{e}") from e

@route.post("/addComment/{postId}")
def addComment(postId:str,content:Comment=Body(...,title="Add Comment"),credentials: HTTPAuthorizationCredentials = AppConstants.jwt_auth()):
    try:
        uniqueId=AppConstants.uniqueid()
        currentDateTime=AppConstants.currentDateTime()
        userInfo=dbUtil.findOneUser({"_id":credentials})
        print(f"Cradentials {credentials} and userInfo is {userInfo}")
        commentData = {
        "_id": uniqueId,
        "dateTime": currentDateTime,
        "content": content.content,
        "userInfo": {
        "_id": userInfo["_id"],
        "firstName": userInfo["firstName"],
        "lastName": userInfo["lastName"]
          }
        }

        updateQuery={"$push":{"comment":{"$each":[commentData],"$position":0}}}
        dbUtil.updateOnePost({"_id":postId},updateQuery)
        return {"message":"Comment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal Server error{e}") from e    

@route.post("/removeComment/{postId}")
def removeComment(postId:str,commentData:CommentUniquId=Body(...,title="Add comment"),credentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
        updateQuery={"$pull":{"comment":{"_id":commentData.commentId}}}
        print(f"CommentId {commentData.commentId}")
        dbUtil.updateOnePost({"_id":postId},updateQuery)
        return {"message":"Comment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal server error{e}") from e
    
@route.get("/getComment/{postId}")
def getComment(postId:str,credentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
        findQuery={"_id":postId}
        postData= dbUtil.findOnePost(findQuery)
        return {"message":"Comments fetched successfully","commentData":postData["comment"]}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal server error{e}") from e
@route.post("/addOrRemoveLike/{postId}")
def addLike(postId:str,cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
        findQuery={"_id":postId}
        postData=dbUtil.findOnePost(findQuery)
        currentUserLike=False
        for like in postData["like"]:
            if like["_id"]==cradentials:
                currentUserLike=True
                break
            
        if currentUserLike:
            queryToUpdateLike={"$pull":{"like":{"_id":cradentials}}}
            dbUtil.updateOnePost(findQuery,queryToUpdateLike)
            return {"message":"Like removed successfully"}
        
        else:
             
         currentDateTime=AppConstants.currentDateTime()
         userInfo=dbUtil.findOneUser({"_id":cradentials})
         likeData={
            "_id":userInfo["_id"],
            "firstName":userInfo["firstName"],
            "lastName":userInfo["lastName"],
            "dateTime":currentDateTime
         }
         updateQuery={"$push":{"like":{"$each":[likeData],"$position":0}}}  
         dbUtil.updateOnePost(findQuery,updateQuery)
         return {"message":"Like added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Internal server error{e}") from e

@route.get("/getPostLike/{postId}")
def getPostLike(postId:str,cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:

      findQuery={"_id":postId}
      postData=dbUtil.findOnePost(findQuery)
      return {"message":"Post liked fetched ssuccessfully","likeData":postData["like"]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal server error{e}") from e
    





