from pydantic import BaseModel,EmailStr

class registrationModel(BaseModel):
    firstName:str
    lastName:str
    email:EmailStr
    password:str

class loginModel(BaseModel):
    email:EmailStr
    password:str    
class updateUserModel(BaseModel):
    firstName:str
    lastName:str    