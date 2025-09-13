import os, hashlib
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import ApiKey

def ensure_bootstrap_api_key():
    raw = os.getenv("BOOTSTRAP_API_KEY")
    if not raw:
        return
    key_hash = hashlib.sha256(raw.encode()).hexdigest()
    db: Session = SessionLocal()
    try:
        exists = db.query(ApiKey).filter(
            ApiKey.key_hash == key_hash,
            ApiKey.is_active == True
        ).first()
        if not exists:
            db.add(ApiKey(name="bootstrap", key_hash=key_hash, is_active=True))
            db.commit()
    finally:
        db.close()
