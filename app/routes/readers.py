from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_reader():
    return "create_reader"

@router.get("/")
def get_readers():
    return "get_readers"

@router.get("/{reader_id}")
def get_reader():
    return "get_reader"

@router.put("/{reader_id}")
def update_reader():
    return "update_reader"

@router.delete("/{reader_id}")
def delete_reader():
    return "delete_reader"
