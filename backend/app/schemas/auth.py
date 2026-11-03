from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class SignupRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("Full name must contain at least 2 characters.")

        return value

    @field_validator("password")
    @classmethod
    def validate_password_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 UTF-8 bytes.")

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password_bytes(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 UTF-8 bytes.")

        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# from datetime import datetime

# from pydantic import BaseModel, ConfigDict, EmailStr, Field


# class SignupRequest(BaseModel):
#     full_name: str = Field(min_length=2, max_length=100)
#     email: EmailStr
#     password: str = Field(min_length=8, max_length=128)


# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str = Field(min_length=1, max_length=128)


# class UserResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     full_name: str
#     email: EmailStr
#     is_active: bool
#     created_at: datetime


# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"
#     user: UserResponse
