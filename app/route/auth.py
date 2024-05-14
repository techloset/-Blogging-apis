from fastapi import APIRouter,Body,HTTPException,status,Depends
from fastapi.security import HTTPAuthorizationCredentials
from app.models import registrationModel,loginModel,updateUserModel
from app.utils import JwtHelper,DatabaseUtil
from app.app_constant import AppConstants
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from pymongo.errors import PyMongoError
route=APIRouter()
dbUtil = DatabaseUtil()

@route.get("/")
def test():
    return {"Hello":"Message"}
@route.post("/register")
def registerUser(userInfo:registrationModel=Body(...,title="Registration of user")):
     """
    Register a new user.

    Args:
        userInfo (registrationModel): User registration information.

    Returns:
        dict: A dictionary containing information about the new user and a token.

    Raises:
        HTTPException: If there's a validation error or the user already exists.
    """
    
     try:
        userInfo.model_dump()
     except:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail="Validation error")   
     userId=AppConstants.uniqueid()
     token=JwtHelper.createJwtToken(userId)
     print(userInfo.password)
     hashedPassword=pbkdf2_sha256.hash(userInfo.password)

     emailExist=dbUtil.findOneUser({
        "email":userInfo.email
    })
     print(emailExist)
     if emailExist:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User already exist")
     else:
        detail={
            "_id":userId,
            "firstName":userInfo.firstName,
            "lastName":userInfo.lastName,
            "email":userInfo.email,
            "password":hashedPassword,
            "dateTime":datetime.now()
        }
        dbUtil.insertOneUser(detail)
        return {"New user":detail,"token":token}

@route.post("/login")
def LoginUser(userInfo:loginModel=Body(...,title="Login of user")):
    """
    Login with user credentials.

    Args:
        userInfo (loginModel): User login information.

    Returns:
        dict: A dictionary containing a success message, token, and user information.

    Raises:
        HTTPException: If there's a validation error, incorrect email/password, or user not found.
    """ 
    try:
        userInfo.model_dump()
    except:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Validation failed") 
    emailOrPasswordExist= dbUtil.findOneUser({"email":userInfo.email})
    print(emailOrPasswordExist)

    if emailOrPasswordExist:
        print(emailOrPasswordExist["password"])
        hashedPassword=emailOrPasswordExist["password"]
        print(userInfo.password)
        verifyHashedPassword=pbkdf2_sha256.verify(userInfo.password,hashedPassword)
        print(verifyHashedPassword)
        print(hashedPassword)
        if verifyHashedPassword:
            token=JwtHelper.createJwtToken(emailOrPasswordExist["_id"])
            return {"message":"Successfully Login","token":token,"existingUser":userInfo}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")

@route.get("/verifyUser")
def verifyUser(cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
   return {"id":cradentials}
@route.get("/getUser")
def getUser(cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    userInfo=dbUtil.findOneUser({"_id":cradentials})
    return userInfo
@route.put("/updateUser")
def updateUser(cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth(),userInfo:updateUserModel=Body(...,title="Update user information")):
    try: 
      updateQuery={"$set":{"firstName":userInfo.firstName,"lastName":userInfo.lastName}}
      dbUtil.updateOneUser({"_id":cradentials},updateQuery)
      return {"message":"Information updated successfully"}
    except PyMongoError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
@route.delete("/deleteUser")
def deleteUser(cradentials:HTTPAuthorizationCredentials=AppConstants.jwt_auth()):
    try:
        findUserQuery={"_id":cradentials}
        findPostQuery={"userId":cradentials}
        dbUtil.deleteOneUser(findUserQuery)
        dbUtil.deleteManyPost(findPostQuery)
        return {"message":"User Deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal server error {e}")



