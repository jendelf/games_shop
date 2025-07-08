from pydantic import BaseModel,ConfigDict, EmailStr, field_validator, Field
import re
class UserBase(BaseModel):
    username: str = Field(..., max_length=100, description="Username is maximum 100 letters")
    email: EmailStr
    disabled: bool = Field(default=False, description="Is account blocked or not")
    balance: float = Field(default=0.0, ge=0)

class UserIn(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must contain at least 8 characters")
        if not re.search(r"[A-Za-z]", value):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>\\/~`\[\]-]", value):
            raise ValueError("Password must contain at least one special symbol")
        return value

class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel): 
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None



