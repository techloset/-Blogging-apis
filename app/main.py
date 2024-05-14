from fastapi import FastAPI
from app.route import auth
from app.route import post
app=FastAPI()
app.include_router(auth.route, prefix="/api/auth",tags=["Authentication"])
app.include_router(post.route, prefix="/api/post",tags=["Posts"])

