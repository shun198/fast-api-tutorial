from enum import Enum
from math import gamma

from fastapi import FastAPI


class ModelName(str, Enum):
    alpha = "alpha"
    beta = "beta"
    gamma = "gamma"


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alpha:
        return {"model_name": model_name, "message": "Alpha is called"}

    if model_name.value == ModelName.beta:
        return {"model_name": model_name, "message": "Beta is called"}

    if model_name.value == ModelName.gamma:
        return {"model_name": model_name, "message": "Gamma is called"}

    return {"model_name": model_name, "message": "Test model message"}
