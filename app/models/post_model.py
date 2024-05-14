from pydantic import BaseModel
from typing import List,Any,Optional
class AddPostModel(BaseModel):
    title:str
    content:str
    tags:List[str]=[]
    category:str
    like:List[Any]=[]
    comment:List[Any]=[]
class Comment(BaseModel):
    content:str
class CommentUniquId(BaseModel):
    commentId:str