import jwt
from datetime import datetime,timedelta
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from fastapi import Depends,status,HTTPException
from app.app_constant import AppConstants
from app.utils import database_utils
import os
class JwtHelper:
    @staticmethod
    def createJwtToken(userId:str):
        expirationTime=datetime.now()+timedelta(days=30)
        payload={
            "userId":userId,
            "exp":expirationTime
        }
        secreteKey=AppConstants.securityKey
        token = jwt.encode(payload,secreteKey,algorithm="HS256")
        return token
    @staticmethod
    def decodeToken(token):
        secreteKey=AppConstants.securityKey 
        payload=jwt.decode(token,secreteKey,algorithms="HS256")
        print(payload)
        return payload
    security=HTTPBearer()
    @staticmethod 
    def verifyToken(credentials:HTTPAuthorizationCredentials=Depends(security)):
        try:
          payload=JwtHelper.decodeToken(credentials.credentials)
          dbUtil=database_utils.DatabaseUtil()
          userInfo=dbUtil.findOneUser({"_id":payload["userId"]})
          if userInfo is None:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
          return payload["userId"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
