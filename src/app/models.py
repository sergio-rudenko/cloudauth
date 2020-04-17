from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.data import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    phone = Column(String(16), unique=True, nullable=False)
    description = Column(String())

    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(DateTime, default=func.now(), nullable=False)

    tokens = relationship("Token", order_by="Token.key", back_populates="user")
    hashes = relationship("Hash", order_by="Hash.key", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    key = Column(String(32), primary_key=True, nullable=False)
    description = Column(String())

    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="tokens")


class Hash(Base):
    __tablename__ = "hashes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    key = Column(String(64), primary_key=True, nullable=False)
    description = Column(String())

    created = Column(DateTime, default=func.now(), nullable=False)
    updated = Column(DateTime, default=func.now(), nullable=False)

    user = relationship("User", back_populates="hashes")
