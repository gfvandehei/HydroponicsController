from pydantic import BaseModel

class RegisterRequest(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str