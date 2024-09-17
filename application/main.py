from datetime import datetime, time, timedelta
from enum import Enum
from typing import Annotated, List, Union
from uuid import UUID

from fastapi import (
    Body,
    Cookie,
    Depends,
    FastAPI,
    File,
    Header,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr


class Item(BaseModel):
    name: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[float, None] = None
    tax: float = 10.5
    tags: List[str] = []


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


app = FastAPI(
    title="FastAPI Tutorial",
    version="0.0.1",
)


@app.get("/api/health", tags=["health"])
async def health_check():
    """ヘルスチェック用のAPI"""
    return {"status": "pass"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/", tags=["items"])
async def read_items(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$"
    ),
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/cookies/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.get("/headers/")
async def read_items(user_agent: Union[str, None] = Header(default=None)):
    return {"User-Agent": user_agent}


@app.get("/items_list/", tags=["items"])
async def read_items(q: List[str] = Query(default=["foo", "bar"])):
    query_items = {"q": q}
    return query_items


@app.get("/items/{item_id}", tags=["items"])
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}", tags=["items"])
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),
    repeat_at: Union[time, None] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/users/{user_id}/items/{item_id}", tags=["user"])
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is an amazing item that has a long description"
            }
        )
    return item


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post(
    "/user/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    tags=["user"],
    response_description="ユーザの作成に成功したとき",
)
async def create_user(user_in: UserIn):
    """
    ユーザを新規作成
    """
    user_saved = fake_save_user(user_in)
    return user_saved


def fake_decode_token(token):
    return UserBase(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user


@app.get("/users/me", tags=["user"])
async def read_users_me(current_user: UserBase = Depends(get_current_user)):
    return current_user


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    for file in files:
        if file.filename.rsplit(".")[-1] != "yml":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="file must be yaml",
            )
    return {"filenames": [file.filename for file in files]}


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The bartenders",
        "price": 62,
        "tax": 20.2,
    },
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
        "tags": [],
    },
}


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items_token/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
