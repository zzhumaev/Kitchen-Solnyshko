from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/stock", tags=["stock"])

@router.get("", response_model=list[schemas.StockRead])
def get_stock(location_id: int | None = None, db: Session = Depends(get_db)):
    q = db.query(models.Stock)
    if location_id:
        q = q.filter(models.Stock.location_id == location_id)
    rows = q.all()
    return [schemas.StockRead(product_id=r.product_id, location_id=r.location_id, qty=float(r.qty)) for r in rows]
