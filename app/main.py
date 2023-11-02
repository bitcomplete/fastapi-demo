import logging
from typing import Annotated, Union
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from fastapi import FastAPI, HTTPException, Query, Path, Request

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



logger = logging.getLogger("uvicorn")
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
class Creature(BaseModel):
    id: int
    family: str
    common_name: str
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "family": "Amphibian",
                "name": "Frog"
            }
        }

class AuthenticationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)

    
creatures: list[Creature] = [Creature(id=1, family="Amphibian", common_name="Frog")]

@app.post("/create_amphibian")
def create_amphibian(creature: Creature, user_level: int, throws: bool = False) -> bool:
    if throws:
        raise Exception("This is an unexpected exception")
    if creature.family != "Amphibian": # validation error not caught by FastAPI
        raise HTTPException(status_code=400, detail="Only amphibians allowed")
    if user_level < 2:
        raise AuthenticationError(detail="You are not admin")
    creatures.append(creature)
    return True    

@app.exception_handler(Exception)
async def _unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("There was an unhandled error")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(HTTPException)
async def _http_exception_handler(request: Request, exc: HTTPException):
    logger.error("There was an handled error")
    
    return await http_exception_handler(request, exc)

@app.exception_handler(AuthenticationError)
async def _authentication_exception_handler(request: Request, exc: AuthenticationError):
    logger.info(str(request.json()))
    logger.error(f"A level {request.user_level} user tried to access a restricted resource")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )




# For local debugging
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)