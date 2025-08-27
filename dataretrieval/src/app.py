from fastapi import FastAPI
from pymongo import MongoClient
import os

def create_app() -> FastAPI:
    "Create a FastAPI app"
    app = FastAPI(title="Data Retrieval API")
    
    mongo_uri = os.getenv("LOCAL_MONGO_URI", "mongodb://localhost:27017/")
    mongo_db = os.getenv("LOCAL_MONGO_DB", "IranMalDBLocal")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
    app.state.mongo_client = client
    app.state.mongo_db = client[mongo_db]
    
    from .routes import register_routes
    
    register_routes(app)
    
    return app