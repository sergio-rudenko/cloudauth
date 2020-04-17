from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, constr


# base -----------------------------------------------------------------------
class UserBase(BaseModel):
    phone: constr(strip_whitespace=True, max_length=16)
    description: constr(strip_whitespace=True)

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    key: constr(strip_whitespace=True, max_length=32)
    description: constr(strip_whitespace=True)

    class Config:
        orm_mode = True


class HashBase(BaseModel):
    key: constr(strip_whitespace=True, max_length=64)
    description: constr(strip_whitespace=True)

    class Config:
        orm_mode = True


# create ---------------------------------------------------------------------
class UserCreate(UserBase):
    pass


class TokenCreate(TokenBase):
    user_phone: constr(strip_whitespace=True, max_length=16)


class HashCreate(HashBase):
    user_phone: constr(strip_whitespace=True, max_length=16)


# value ----------------------------------------------------------------------
class Token(TokenBase):
    created: datetime
    updated: datetime
    user: UserBase

    class Config:
        orm_mode = True


class Hash(HashBase):
    created: datetime
    updated: datetime
    user: UserBase

    class Config:
        orm_mode = True


class TokenOut(TokenBase):
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class HashOut(HashBase):
    created: datetime
    updated: datetime

    class Config:
        orm_mode = True


class User(UserBase):
    created: datetime
    updated: datetime
    tokens: List[TokenOut] = []
    hashes: List[HashOut] = []

    class Config:
        orm_mode = True
