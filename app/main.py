import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from starlette.responses import JSONResponse
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

from database.mongodb import MongoDB
from config.development import config
from model.student import createStudentModel, updateStudentModel

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


@app.get("/")
def index():
    return JSONResponse(content={"message": "Student Info"}, status_code=200)


@app.get("/students/")
def get_students(
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, min_length=3, max_length=4),
):

    try:
        result = mongo_db.find(sort_by, order)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.get("/students/{student_id}")
def get_students_by_id(student_id: str = Path(None, min_length=10, max_length=10)):
    try:
        result = mongo_db.find_one(student_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if result is None:
        raise HTTPException(status_code=404, detail="Student Id not found !!")

    return JSONResponse(
        content={"status": "OK", "data": result},
        status_code=200,
    )


@app.post("/students")
def create_books(student: createStudentModel):
    try:
        student_id = mongo_db.create(student)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "student_id": student_id,
            },
        },
        status_code=201,
    )


@app.patch("/students/{student_id}")
def update_books(
    student: updateStudentModel,
    student_id: str = Path(None, min_length=10, max_length=10),
):
    print("student", student)
    try:
        updated_student_id, modified_count = mongo_db.update(student_id, student)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Student Id: {updated_student_id} is not update want fields",
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "student_id": updated_student_id,
                "modified_count": modified_count,
            },
        },
        status_code=200,
    )


@app.delete("/students/{student_id}")
def delete_book_by_id(student_id: str = Path(None, min_length=10, max_length=10)):
    try:
        deleted_student_id, deleted_count = mongo_db.delete(student_id)
    except:
        raise HTTPException(status_code=500, detail="Something went wrong !!")

    if deleted_count == 0:
        raise HTTPException(
            status_code=404, detail=f"Student Id: {deleted_student_id} is not Delete"
        )

    return JSONResponse(
        content={
            "status": "ok",
            "data": {
                "student_id": deleted_student_id,
                "deleted_count": deleted_count,
            },
        },
        status_code=200,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)
