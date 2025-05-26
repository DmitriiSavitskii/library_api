from fastapi import APIRouter

router = APIRouter()

@router.post("/",)
def create_book():
    return "create_book"

@router.get("/")
def get_books():
    return "get_books"

@router.get("/{book_id}")
def get_book():
    return "get_book"

@router.put("/{book_id}")
def update_book():
    return "update_book"

@router.delete("/{book_id}")
def delete_book():
    return "delete_book"
