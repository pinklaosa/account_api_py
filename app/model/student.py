from typing import Optional, List
from pydantic import BaseModel, Field


class createStudentModel(BaseModel):
    id: str = Field(min_length=10, max_length=10)
    first_name: str
    last_name: str
    email: str
    gender: str
    age: int
    picture_url: str
    height: int
    weight: float
    hobby: List[str]
    country: str
    city: str


class updateStudentModel(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    height: Optional[int]
    weight: Optional[float]
    hobby: Optional[List[str]]
    country: Optional[str]
    city: Optional[str]
