from typing import Optional, List
from pydantic import BaseModel, Field


class createAccountModel(BaseModel):
    username: str = Field(min_length=6, max_length=15)
    password: str
    first_name: str
    last_name: str
    email: str
    phone: str


class updateAccountModel(BaseModel):
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
