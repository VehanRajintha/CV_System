from database import SessionLocal
import models
from auth import verify_password

def check_admin():
    db = SessionLocal()
    try:
        # Try to find admin user
        admin = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        if not admin:
            print("Admin user does not exist!")
            return
        
        print("Admin user found:")
        print(f"Email: {admin.email}")
        print(f"Name: {admin.name}")
        print(f"Is Admin: {admin.is_admin}")
        
        # Test password
        test_password = "admin123"
        if verify_password(test_password, admin.hashed_password):
            print("Password is correct!")
        else:
            print("Password is incorrect!")
            
    except Exception as e:
        print(f"Error checking admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin() 