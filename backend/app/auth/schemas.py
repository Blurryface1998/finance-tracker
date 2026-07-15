from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from . import utils


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username", mode="before")
    @classmethod
    def username_validator(cls, value: str) -> str:
        return utils.validate_username(value)

    @field_validator("email", mode="before")
    @classmethod
    def email_validator(cls, value: str) -> str:
        return utils.validate_email(value)

    @field_validator("password", mode="before")
    @classmethod
    def password_validator(cls, value: str) -> str:
        return utils.validate_password(value)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email", mode="before")
    @classmethod
    def email_validator(cls, value: str) -> str:
        return utils.validate_email(value)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
