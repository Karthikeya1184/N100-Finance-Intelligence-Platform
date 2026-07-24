from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_companies():
    return {"message": "Companies endpoint"}