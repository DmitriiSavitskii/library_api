from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
def register():
    return "register"


@router.post("/login")
def login():
    return "login"
