import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import MongoDB
from config.development import config
from model.account import createAccountModel, updateAccountModel

mongo_config = config["mongo_config"]
mongo_db = MongoDB(
    mongo_config["host"],
    mongo_config["port"],
    mongo_config["user"],
    mongo_config["password"],
    mongo_config["auth_db"],
    mongo_config["db"],
    mongo_config["collection"],
)
mongo_db._connect()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http method [get(เรียกดู) , post(เพิ่ม) , [put , patch(อัพเดต)] , delete(ลบ)]

# this is Get method
@app.get("/")
def index():
    return JSONResponse(content={"message": "Connected 2"}, status_code=200)


@app.get("/profile/")
def get_students(
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, min_length=3, max_length=4),
):
    try:
        # calling function "find" from mongodb.py
        result = mongo_db.find(sort_by, order)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


# This get with username
@app.get("/profile/{username}")
def get_students_by_id(username: str = Path(None, min_length=6, max_length=15)):
    try:
        # calling function "find_one" for get username's index
        result = mongo_db.find_one(username)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if result is None:
        raise HTTPException(status_code=404, detail="Student Id not found !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


# This post for insert data
@app.post("/profile")
def create_books(account: createAccountModel):
    try:
        account_username = mongo_db.create(account)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "username": account_username,
            },
        },
        status_code=201,
    )


# This patch for update data
@app.patch("/profile/{username}")
def update_books(
    update_account: updateAccountModel,
    username: str = Path(None, min_length=6, max_length=15),
):
    print("account", update_account)
    try:
        updated_username, modified_count = mongo_db.update(username, update_account)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"account Id: {updated_username} is not update want fields",
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "username": updated_username,
                "modified_count": modified_count,
            },
        },
        status_code=200,
    )


@app.delete("/profile/{username}")
def delete_book_by_id(username: str = Path(None, min_length=10, max_length=10)):
    try:
        deleted_username, deleted_count = mongo_db.delete(username)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Student Id: {deleted_username} is not Delete"
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "username": deleted_username,
                "deleted_count": deleted_count,
            },
        },
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)
