from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=list[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id).all()

@router.post("", response_model=schemas.ProductRead)
def create_product(body: schemas.ProductCreate, db: Session = Depends(get_db)):
    # проверим, что unit существует
    unit = db.query(models.Unit).get(body.unit_id)
    if not unit:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Unit {body.unit_id} does not exist")

    p = models.Product(**body.model_dump())
    db.add(p)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Product violates a constraint (likely duplicate)")
    db.refresh(p)
    return p
