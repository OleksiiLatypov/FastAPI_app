import uvicorn
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from fastapi_limiter.depends import RateLimiter
from src.routes import contacts, users, auth
from src.conf.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

origins = [
    "http://localhost:3000", "http://127.0.0.1:5000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/healthchecker')
async def check():
    return {'message': 'Welcome to FastAPI'}


@app.get('/')
async def root():
    return {'message': 'Hello Oleksii Latypov'}


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
