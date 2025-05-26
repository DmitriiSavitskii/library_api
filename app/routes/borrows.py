from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def borrow_book():
    return "borrow_book"