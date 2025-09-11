from fastapi import FastAPI, Response
from .db import engine, Base
from .routers import units, products, locations, stock, documents
from fastapi import FastAPI
from app.routers import reports

app = FastAPI()
app.include_router(reports.router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.head("/health")
def health_head():
    return Response(status_code=200)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
@app.get("/ping")
def ping():
    return {"ping": "pong"}

app.include_router(units.router)
app.include_router(products.router)
app.include_router(locations.router)
app.include_router(stock.router)
app.include_router(documents.router)
