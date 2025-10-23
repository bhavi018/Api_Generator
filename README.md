# 🚀 FastAPI Code Generator with Authentication & SQLAlchemy

A professional **FastAPI CRUD Code Generator** that automatically generates production-ready API code with authentication, database integration, and a beautiful Streamlit UI for testing and management.

---

## ✨ Features

### Core Functionality

- 🏢 **Multi-Organization Support** - Generate isolated APIs for different organizations
- 🔐 **JWT Authentication** - Secure endpoints with role-based access control (Admin/User)
- 💾 **SQLAlchemy ORM** - Complete database integration with SQLite
- 🎨 **Beautiful UI** - Professional Streamlit interface with modern design
- 📝 **Code Generation** - Auto-generate complete FastAPI CRUD applications
- 🧪 **Live Testing** - Test generated APIs directly from the UI
- 📥 **Code Export** - Download generated code as Python files

### Technical Features

- **CRUD Operations**: Create, Read, Update, Delete users
- **Session Management**: Persistent authentication across requests
- **Error Handling**: Comprehensive error messages and validation
- **Database Migrations**: Automatic table creation
- **API Key Generation**: Unique keys per organization
- **Token-based Auth**: Secure JWT implementation

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Streamlit UI   │ ← User Interface
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   FastAPI       │ ← Backend API
│   Application   │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌──────────┐
│ SQLite │ │   JWT    │
│   DB   │ │  Auth    │
└────────┘ └──────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Clone the Repository

```bash
git clone https://github.com/bhavi018/Api_Generator_Chatbot.git
cd Api_Generator_Chatbot
```

### Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create `requirements.txt`

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
streamlit==1.28.1
requests==2.31.0
python-multipart==0.0.6
```

---

## 🚀 Usage

### 1. Start the FastAPI Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Launch the Streamlit UI

In a new terminal:

```bash
streamlit run streamlit_app.py
```

The UI will open automatically at `http://localhost:8501`

### 3. Generate Your First API

#### Step 1: Login

- Enter your Organization ID
- Select your role (admin/user)
- Click "Login"

#### Step 2: Create Organization

- Enter organization name
- Click "Create Organization"
- Save your Org ID and API Key

#### Step 3: Generate Code

- Click "Generate Code"
- View the auto-generated FastAPI code
- Download the code file

#### Step 4: Test API

- Select CRUD operation
- Fill in user details
- Click "Run Test"
- View response

---

### User CRUD Endpoints

All user endpoints require JWT authentication via `Authorization: Bearer <token>` header.

#### `POST /api/org/{org_id}/users/`

Create a new user (Admin only)

#### `GET /api/org/{org_id}/users/{user_id}`

Retrieve user details

#### `PUT /api/org/{org_id}/users/{user_id}`

Update user information (Admin only)

#### `DELETE /api/org/{org_id}/users/{user_id}`

Delete a user (Admin only)

---

## 🛠️ Technologies Used

### Backend

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type hints
- **Python-JOSE** - JavaScript Object Signing and Encryption for JWT
- **Uvicorn** - Lightning-fast ASGI server

### Frontend

- **Streamlit** - Interactive data apps framework
- **Requests** - HTTP library for API calls

### Database

- **SQLite** - Lightweight, file-based database

---

## 🔒 Security Considerations

⚠️ **Important for Production:**

1. **Environment Variables**: Move secrets to `.env` file

   ```python
   SECRET_KEY = os.getenv("SECRET_KEY")
   ```

2. **Password Hashing**: Implement proper password hashing

   ```bash
   pip install passlib bcrypt
   ```

3. **HTTPS**: Always use HTTPS in production

4. **Rate Limiting**: Add rate limiting to prevent abuse

   ```bash
   pip install slowapi
   ```

5. **CORS**: Configure CORS properly
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   ```

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- Streamlit for the amazing UI framework
- SQLAlchemy for database management
- All contributors and supporters

---
