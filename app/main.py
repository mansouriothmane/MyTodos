from fastapi import FastAPI
from app.routers import task, auth

app = FastAPI()

app.include_router(task.router, tags=["Tasks"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
