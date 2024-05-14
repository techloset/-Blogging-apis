import uvicorn
from app.main import app
from app.app_constant import AppConstants
from dotenv import load_dotenv

if __name__=="__main__":
    load_dotenv()
    AppConstants.db
    print("welcome to pymongo")    
    uvicorn.run(app,host="127.0.0.1",port=8000)

