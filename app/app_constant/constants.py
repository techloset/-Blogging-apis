from app.utils import ConnectionUtil
from app.utils import jwt_util
from datetime import datetime
from fastapi import Depends
import uuid
class AppConstants:
    db=ConnectionUtil()
    securityKey="SECRET_KEY"
    @staticmethod
    def jwt_auth():
        return Depends(jwt_util.JwtHelper.verifyToken)
    @staticmethod
    def uniqueid()->str:
        return str(uuid.uuid4())
    @staticmethod
    def currentDateTime():
        return datetime.now()