from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import task, user, auth

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
