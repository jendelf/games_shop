from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field
import re
from .models import Role

class UserIn(BaseModel):
    username: str = Field(..., max_length=100, description="Username is maximum 100 letters")
    email: EmailStr
    password: str
    role: Role = Role.CUSTOMER

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


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    disabled: bool
    balance: float
    role: Role

    model_config = ConfigDict(from_attributes=True)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: EmailStr | None = None
