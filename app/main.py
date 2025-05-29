import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import auth, books, borrows, readers


app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(readers.router, prefix="/readers", tags=["readers"])
app.include_router(borrows.router, prefix="/borrows", tags=["borrows"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Library API",
        version="1.0.0",
        description="API для управления библиотекой с аутентификацией",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
