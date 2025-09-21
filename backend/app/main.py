# backend/app/main.py
from fastapi import FastAPI
from .api import router


app = FastAPI(title="Career Trends API")
app.include_router(router, prefix="/api")


if __name__ == '__main__':
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)