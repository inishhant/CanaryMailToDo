from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import tasks

app = FastAPI()

# 🔥 CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or ["*"] if you're cool with all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB setup
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(tasks.router)
