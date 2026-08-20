from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from . import utils


class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    password: str

    @field_validator("name", mode="before")
    @classmethod
    def name_validator(cls, value: str) -> str:
        return utils.validate_name(value, max_length=50, field_name="Name")

    @field_validator("last_name", mode="before")
    @classmethod
    def last_name_validator(cls, value: str) -> str:
        return utils.validate_name(value, max_length=100, field_name="Last name")

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
    name: str
    last_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    message: str
