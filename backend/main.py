from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from datetime import timedelta
import shutil

from database import get_db, engine
import models
from auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, get_current_admin, ACCESS_TOKEN_EXPIRE_MINUTES
)
from cv_encryption import generate_key, encrypt_file, decrypt_file

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Type"]
)

# Create necessary directories
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "CV Management System API"}

@app.post("/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        db_user = db.query(models.User).filter(models.User.email == email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = get_password_hash(password)
        db_user = models.User(email=email, name=name, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload-cv")
async def upload_cv(
    job_title: str = Form(...),
    industry: str = Form(...),
    cv_file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Save the file
        file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{cv_file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(cv_file.file, buffer)
        
        # Encrypt the file
        encryption_key = generate_key()
        encrypted_file_path = encrypt_file(file_path, encryption_key)
        
        # Remove the original file
        os.remove(file_path)
        
        # Save CV entry to database
        db_cv = models.CV(
            job_title=job_title,
            industry=industry,
            cv_file_path=encrypted_file_path,
            encrypted_key=encryption_key.decode(),
            user_id=current_user.id
        )
        db.add(db_cv)
        db.commit()
        db.refresh(db_cv)
        
        return {"message": "CV uploaded successfully"}
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/download-cv/{cv_id}")
async def download_cv(
    cv_id: int,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        # Get CV from database
        cv = db.query(models.CV).filter(models.CV.id == cv_id).first()
        if not cv:
            raise HTTPException(status_code=404, detail="CV not found")

        # Get original filename from the encrypted file path
        original_filename = os.path.basename(cv.cv_file_path).replace('.encrypted', '')
        
        # Create temp file path for decrypted file
        temp_file_path = os.path.join(TEMP_DIR, f"decrypted_{cv_id}_{original_filename}")
        
        # Decrypt the file
        decrypt_file(cv.cv_file_path, cv.encrypted_key.encode(), temp_file_path)
        
        # Return the file as a download
        headers = {
            'Content-Disposition': f'attachment; filename="{original_filename}"'
        }
        
        return FileResponse(
            temp_file_path,
            headers=headers,
            media_type='application/octet-stream',
            filename=original_filename
        )
    except Exception as e:
        print(f"Download error: {str(e)}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp directory
        if os.path.exists(TEMP_DIR):
            shutil.rmtree(TEMP_DIR)
            os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/admin/dashboard")
async def admin_dashboard(
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        total_cvs = db.query(models.CV).count()
        cvs = db.query(models.CV).join(models.User).all()
        
        cv_list = []
        for cv in cvs:
            original_filename = os.path.basename(cv.cv_file_path).replace('.encrypted', '')
            cv_list.append({
                "id": cv.id,
                "job_title": cv.job_title,
                "industry": cv.industry,
                "upload_date": cv.upload_date,
                "user_email": cv.user.email,
                "user_name": cv.user.name,
                "filename": original_filename
            })
        
        return {
            "total_cvs": total_cvs,
            "cv_list": cv_list
        }
    except Exception as e:
        print(f"Admin dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/dashboard")
async def user_dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        user_cvs = db.query(models.CV).filter(models.CV.user_id == current_user.id).all()
        cv_list = []
        for cv in user_cvs:
            cv_list.append({
                "id": cv.id,
                "job_title": cv.job_title,
                "industry": cv.industry,
                "upload_date": cv.upload_date
            })
        
        return {
            "user": {
                "email": current_user.email,
                "name": current_user.name
            },
            "cvs": cv_list
        }
    except Exception as e:
        print(f"User dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 