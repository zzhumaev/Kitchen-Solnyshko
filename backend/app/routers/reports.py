from fastapi import APIRouter

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/health")
def health():
    return {"status": "ok"}
