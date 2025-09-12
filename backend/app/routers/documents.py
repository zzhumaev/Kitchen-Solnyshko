from decimal import Decimal
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("", response_model=schemas.DocumentRead)
def create_document(body: schemas.DocumentCreate, db: Session = Depends(get_db)):
    doc = models.Document(type=models.DocType(body.type), created_by=body.created_by)
    db.add(doc); db.flush()

    for item in body.items:
        di = models.DocItem(
            doc_id=doc.id, product_id=item.product_id,
            location_id=item.location_id, qty=item.qty
        )
        db.add(di)
        st = db.query(models.Stock).filter_by(
            product_id=item.product_id, location_id=item.location_id
        ).first()
        if not st:
            st = models.Stock(product_id=item.product_id, location_id=item.location_id, qty=0)
            db.add(st); db.flush()
        if body.type == "in":
            st.qty = (st.qty or Decimal("0")) + Decimal(str(item.qty))
        elif body.type == "out":
            st.qty = (st.qty or 0) - item.qty
        elif body.type == "invent":
            st.qty = item.qty

    db.commit(); db.refresh(doc)
    return doc
