from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("", response_model=list[schemas.LocationRead])
def list_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).order_by(models.Location.name).all()

@router.post("", response_model=schemas.LocationRead)
def create_location(body: schemas.LocationCreate, db: Session = Depends(get_db)):
    l = models.Location(**body.model_dump())
    db.add(l); db.commit(); db.refresh(l)
    return l
