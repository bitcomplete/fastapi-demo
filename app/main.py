from typing import Annotated, Union
import uvicorn

from fastapi import FastAPI, Query, Path

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}


@app.get("/items/{item_id}", tags=["items"])
def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: Annotated[Union[str, None], Query(alias="item-query", max_length=6)] = None
):
    return {"item_id": item_id, "q": q}

# For local debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)