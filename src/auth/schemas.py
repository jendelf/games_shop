from pydantic import BaseModel, EmailStr, field_validator, Field
import re

class UserIn(BaseModel): # user registration 
    username: str = Field(..., max_length=100, description="Username is maximum 100 letters")
    password: str
    email: EmailStr
    full_name: str | None = None

    @field_validator ("password")
    @classmethod
    def validate_password(cls, value:str) -> str:
        if len(value) < 8:
            raise ValueError("Password must contain at least 8 characters")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>\\/~`[\]-]", value):
            raise ValueError("Password must contain at least one special symbol")
        return value
    


class UserOut(BaseModel): #
    username: str
    email: EmailStr
    full_name: str | None = None

class UserLogin(BaseModel): # model for login
    email : EmailStr
    password: str

class Token(BaseModel): #
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

class UserInDB(UserIn):
    hashed_password: str

class EmailPasswordForm(BaseModel):
    email: EmailStr
    password: str
