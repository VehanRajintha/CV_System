from database import SessionLocal
import models
from auth import get_password_hash

def recreate_admin():
    db = SessionLocal()
    try:
        # Delete existing admin if exists
        admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if admin:
            db.delete(admin)
            db.commit()
            print("Deleted existing admin user")
        
        # Create new admin user
        hashed_password = get_password_hash("admin123")
        new_admin = models.User(
            email="admin@example.com",
            name="Admin User",
            hashed_password=hashed_password,
            is_admin=True
        )
        db.add(new_admin)
        db.commit()
        print("\nNew admin user created successfully!")
        print("----------------------------------------")
        print("Email: admin@example.com")
        print("Password: admin123")
        print("----------------------------------------")
        
    except Exception as e:
        print(f"Error recreating admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    recreate_admin() 