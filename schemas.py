from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    fullName: str
    phoneNumber: str
    loggedInAs: str
    isLoggedIn: bool


class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    fullName: str
    phoneNumber: str
    loggedInAs: str
    isLoggedIn: bool

    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    userId: int
    fullName: str
    phoneNumber: str
    details: str
    longitude: str
    latitude: str
    imageUri: Optional[str]


class ReportResponse(BaseModel):
    id: int
    userId: int
    fullName: str
    phoneNumber: str
    details: str
    longitude: str
    latitude: str
    imageUri: Optional[str]
    dateCreated: datetime

    class Config:
        from_attributes = True
