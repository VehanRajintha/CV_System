# CV Management System

A secure CV management system with separate user and admin interfaces, built using FastAPI (backend) and Next.js (frontend).

## Features

- 🔐 Secure user authentication
- 👥 Separate user and admin interfaces
- 📁 Encrypted CV storage
- 📤 CV upload functionality
- 📥 Secure CV download for admins
- 🔍 CV management dashboard
- 🛡️ Role-based access control

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- MySQL
- Python-Jose (JWT)
- Cryptography
- Uvicorn

### Frontend
- Next.js 13+
- TypeScript
- Tailwind CSS
- Framer Motion
- Heroicons

## Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL Server
- Git

## Setup Instructions

### 1. Database Setup
```sql
CREATE DATABASE cv_system;
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "MYSQL_URL=mysql+pymysql://root:@localhost/cv_system" > .env
echo "SECRET_KEY=your-super-secret-key-change-this-in-production" >> .env

# Start backend server
python -m uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start frontend development server
npm run dev
```

## Directory Structure
```
.
├── backend/
│   ├── uploads/           # Encrypted CV storage
│   ├── temp/             # Temporary files for download
│   ├── requirements.txt  # Python dependencies
│   ├── main.py          # Main FastAPI application
│   ├── models.py        # Database models
│   ├── database.py      # Database configuration
│   ├── auth.py          # Authentication logic
│   └── cv_encryption.py # CV encryption/decryption
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── admin/       # Admin dashboard
    │   │   ├── dashboard/   # User dashboard
    │   │   ├── login/       # Login page
    │   │   └── register/    # Registration page
    │   └── components/      # Reusable components
    └── package.json
```

## API Endpoints

### Authentication
- POST `/token` - Login
- POST `/register` - User registration

### User Routes
- GET `/user/dashboard` - User dashboard
- POST `/upload-cv` - Upload CV

### Admin Routes
- GET `/admin/dashboard` - Admin dashboard
- GET `/admin/download-cv/{cv_id}` - Download CV

## Security Features

1. **Password Security**
   - Bcrypt password hashing
   - Secure password storage

2. **CV Security**
   - File encryption using Fernet
   - Secure key management
   - Temporary file cleanup

3. **Authentication**
   - JWT-based authentication
   - Role-based access control
   - Token expiration

## Default Admin Account
```
Email: admin@example.com
Password: admin123
```

## Scripts
- `check_admin.py` - Check admin user status
- `create_admin.py` - Create default admin user
- `recreate_admin.py` - Recreate admin user if needed

## Important Notes

1. **Environment Variables**
   - Update `SECRET_KEY` in production
   - Configure proper database credentials

2. **Production Deployment**
   - Enable HTTPS
   - Update CORS settings
   - Use proper database credentials
   - Change default admin credentials

3. **File Storage**
   - Configure proper file storage paths
   - Regular backup of encrypted files
   - Monitor storage space

## Troubleshooting

1. **Database Connection Issues**
   - Verify MySQL is running
   - Check database credentials
   - Ensure database exists

2. **File Upload Issues**
   - Check directory permissions
   - Verify upload directory exists
   - Check file size limits

3. **Admin Access Issues**
   - Run `check_admin.py`
   - Use `recreate_admin.py` if needed

## License

MIT License - Feel free to use this project for personal or commercial purposes. 