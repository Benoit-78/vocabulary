"""
    Creation date:
        12 January 2025
    Main purpose:
        Provide with pydantic model for the user part of the API.
"""


from pydantic import BaseModel, Field, validator


class Token(BaseModel):
    """
    Base model class for the token.
    """
    access_token: str
    token_type: str



class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

    @validator("username")
    def validate_username(cls, value):
        if not value:
            raise ValueError("Username cannot be empty")
        return value

    @validator("password")
    def validate_password(cls, value):
        if not value:
            raise ValueError("Password cannot be empty")
        return value
