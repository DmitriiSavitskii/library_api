import uvicorn
from fastapi import FastAPI
from app.routes import auth, books, borrows, readers

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(readers.router, prefix="/readers", tags=["readers"])
app.include_router(borrows.router, prefix="/borrows", tags=["borrows"])

@app.get("/")
def home():
    return {"message": "hello, world"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)