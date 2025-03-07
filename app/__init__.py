from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import auth_router
from app.routes.book import book_router
from app.routes.brrow import borrow_router
from app.database import engine, Base
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth")
app.include_router(book_router, prefix="/library")
app.include_router(borrow_router, prefix="/borrow")
