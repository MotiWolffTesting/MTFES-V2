from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse


def register_routes(app: FastAPI) -> None:
    router = APIRouter()

    @router.get("/tweets/antisemitic")
    def get_antisemitic():
        try:
            db = app.state.mongo_db
            cursor = db["tweets_antisemitic"].find({}, {"_id": 0}).sort("createdate", -1).limit(1000)
            return JSONResponse(list(cursor))
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"Mongo unavailable: {exc}")

    @router.get("/tweets/not_antisemitic")
    def get_not_antisemitic():
        try:
            db = app.state.mongo_db
            cursor = db["tweets_not_antisemitic"].find({}, {"_id": 0}).sort("createdate", -1).limit(1000)
            return JSONResponse(list(cursor))
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"Mongo unavailable: {exc}")

    app.include_router(router, prefix="/api")
