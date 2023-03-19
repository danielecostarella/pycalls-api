from app import models, contact, call, findcontact
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contact.router, tags=['Contacts'], prefix='/api/contacts')

app.include_router(call.router, tags=['Calls'], prefix='/api/calls')

app.include_router(findcontact.router, tags=['Find number'], prefix='/api/find-contact-by-number')

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
