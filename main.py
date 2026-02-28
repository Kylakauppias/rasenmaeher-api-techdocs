from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import fastapi
import datetime

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    api_version = "2.7.4"
    release_date = datetime.date.today()
    fastapi_version = fastapi.__version__
    version_string = f"{api_version} ({release_date.strftime('%b %d, %Y')})"
    openapi_schema = get_openapi(
        title=app.title,
        version=version_string,
        description=app.description,
        routes=app.routes,
    )

    openapi_schema["x-generated-date"] = datetime.datetime.now().isoformat()
    openapi_schema["x-fastapi-version"] = fastapi_version
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}

@app.patch("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "item": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id, "deleted": True}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
