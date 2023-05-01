import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/api/healthchecker')
async def check():
    return {'message': 'Welcome to FastAPI'}


@app.get('/')
async def root():
    return {'message': 'Hello Oleksii Latypov'}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
