from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form, Body
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal
import os
import shutil
import uuid
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "Congratulations! Your backend is running 🚀"}


@app.post("/api/v1/login", response_model=schemas.UserResponse)
def login(
    username: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db),
):
    # Find user by username
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or user.password != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return user


@app.post("/api/v1/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(models.User).filter(models.User.username == user.username).first()
    )

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/api/v1/reports", response_model=schemas.ReportResponse)
async def create_report(
    userId: int = Form(...),
    fullName: str = Form(...),
    phoneNumber: str = Form(...),
    details: str = Form(...),
    longitude: str = Form(...),
    latitude: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    image_path = None

    if image:
        # Get file extension (.jpg, .png, etc.)
        file_extension = os.path.splitext(image.filename)[1]

        # Generate unique filename
        unique_filename = (
            f"{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}{file_extension}"
        )

        file_location = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = f"/uploads/{unique_filename}"

    new_report = models.Report(
        userId=userId,
        fullName=fullName,
        phoneNumber=phoneNumber,
        details=details,
        longitude=longitude,
        latitude=latitude,
        imageUri=image_path,
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


@app.get("/api/v1/reports", response_model=list[schemas.ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return db.query(models.Report).all()


@app.get("/api/v1/users/{user_id}/reports", response_model=list[schemas.ReportResponse])
def get_reports_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Report).filter(models.Report.userId == user_id).all()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        reload=False,
    )
