from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    fullName = Column(String)
    phoneNumber = Column(String)
    phoneNumber = Column(String)
    loggedInAs = Column(String, default="")
    isLoggedIn = Column(Boolean, default=False)

    reports = relationship("Report", back_populates="user")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    fullName = Column(String)
    phoneNumber = Column(String)
    details = Column(String)
    longitude = Column(String)
    latitude = Column(String)
    imageUri = Column(String, nullable=True)
    dateCreated = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reports")
