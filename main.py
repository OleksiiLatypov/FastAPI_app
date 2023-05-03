import uvicorn
from fastapi import FastAPI

from src.routes import auth

app = FastAPI()


@app.get('/api/healthchecker')
async def check():
    return {'message': 'Welcome to FastAPI'}


@app.get('/')
async def root():
    return {'message': 'Hello Oleksii Latypov'}


app.include_router(auth.router, prefix='/api')
#app.include_router(contacts.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)
