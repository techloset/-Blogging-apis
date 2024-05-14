from fastapi import FastAPI
from app.route import auth
from app.route import post
from starlette.responses import JSONResponse

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application with Bloggin app",
    version="1.0.0"
)
@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(status_code=404, content={"message": "Route Not found"})
app.include_router(
    auth.route,
    prefix="/api/auth",
    tags=["Authentication"],

)

app.include_router(
    post.route,
    prefix="/api/post",
    tags=["Posts"],
)
