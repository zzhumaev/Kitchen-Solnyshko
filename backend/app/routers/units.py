from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/units", tags=["units"])

@router.get("", response_model=list[schemas.UnitRead])
def list_units(db: Session = Depends(get_db)):
    return db.query(models.Unit).order_by(models.Unit.name).all()

@router.post("", response_model=schemas.UnitRead)
def create_unit(body: schemas.UnitCreate, db: Session = Depends(get_db)):
    u = models.Unit(**body.model_dump())
    db.add(u)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Unit with this name already exists",
        )
    db.refresh(u)
    return u
