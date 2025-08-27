from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routes import router  

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(title="FastAPI SQLite TODO", lifespan=lifespan)
app.include_router(router)

@app.get("/")
async def root():
    return {"msg": "Hello — FastAPI Async TODO"}