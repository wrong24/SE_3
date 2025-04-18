from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime, timedelta
import jwt
import sqlite3
import bcrypt

app = FastAPI()

# JWT Configuration
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize SQLite database for users
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password_hash TEXT,
                  full_name TEXT,
                  email TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

class User(BaseModel):
    username: str
    password: str
    full_name: Optional[str] = None
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# Active user sessions
active_sessions: Dict[str, datetime] = {}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        if username not in active_sessions:
            raise HTTPException(status_code=401, detail="Session expired")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return username

@app.post("/register")
async def register_user(user: User):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # Check if username exists
        c.execute('SELECT username FROM users WHERE username = ?', (user.username,))
        if c.fetchone():
            raise HTTPException(status_code=400, detail="Username already registered")
        
        # Hash password
        password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert new user
        c.execute('''INSERT INTO users (username, password_hash, full_name, email)
                     VALUES (?, ?, ?, ?)''',
                  (user.username, password_hash.decode('utf-8'), user.full_name, user.email))
        conn.commit()
        conn.close()
        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password_hash FROM users WHERE username = ?', (form_data.username,))
        result = c.fetchone()
        conn.close()

        if not result:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        stored_password_hash = result[0].encode('utf-8')
        if not bcrypt.checkpw(form_data.password.encode('utf-8'), stored_password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Create access token
        access_token = create_access_token({"sub": form_data.username})
        active_sessions[form_data.username] = datetime.utcnow()
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logout")
async def logout(current_user: str = Depends(get_current_user)):
    if current_user in active_sessions:
        del active_sessions[current_user]
    return {"message": "Logged out successfully"}

@app.get("/session")
async def get_session_info(current_user: str = Depends(get_current_user)):
    if current_user in active_sessions:
        return {
            "username": current_user,
            "login_time": active_sessions[current_user],
            "session_duration": (datetime.utcnow() - active_sessions[current_user]).seconds
        }
    raise HTTPException(status_code=401, detail="No active session")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)