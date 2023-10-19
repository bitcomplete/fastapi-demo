from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_read_item():
    response = client.get("/items/5?item-query=query")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": "query"}

def test_read_item_no_query():
    response = client.get("/items/5")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "q": None}

def test_read_item_id_too_large():
    response = client.get("/items/1001")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
            "type": "less_than_equal",
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "Input should be less than or equal to 1000",
            "input": "1001",
            "ctx": {
                "le": 1000
            },
            "url": "https://errors.pydantic.dev/2.4/v/less_than_equal"
            }
        ]
    }

def test_read_item_id_not_int():
    response = client.get("/items/foo")
    assert response.status_code == 422
    assert response.json() == {
        "detail":[
            {
                "type":"int_parsing",
                "loc":[
                    "path",
                    "item_id"
                ],
                "msg":"Input should be a valid integer, unable to parse string as an integer",
                "input":"foo",
                "url":"https://errors.pydantic.dev/2.4/v/int_parsing"
            }
        ]
    }

def test_read_item_query_too_long():
    response = client.get("/items/5?item-query=somequerytoolong")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
            "type": "string_too_long",
            "loc": [
                "query",
                "item-query"
            ],
            "msg": "String should have at most 6 characters",
            "input": "somequerytoolong",
            "ctx": {
                "max_length": 6
            },
            "url": "https://errors.pydantic.dev/2.4/v/string_too_long"
            }
        ]
    }