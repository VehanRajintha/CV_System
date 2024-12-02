from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create new admin user
        hashed_password = get_password_hash("admin123")
        admin_user = models.User(
            email="admin@example.com",
            name="Admin User",
            hashed_password=hashed_password,
            is_admin=True
        )
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin@example.com")
        print("Password: admin123")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 