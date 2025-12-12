from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    username: Optional[str] = Field(default=None, max_length=100)
    registration_date: datetime = Field(default_factory=datetime.utcnow)
    subscription_type: str = Field(default='free', max_length=20)
    subscription_expiry: Optional[date] = Field(default=None)
    country_code: Optional[str] = Field(default=None, max_length=2)
    playlists: List["Playlist"] = Relationship(back_populates="creator")
    liked_tracks: List["UserLike"] = Relationship(back_populates="user")
    listening_history: List["ListeningHistory"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user")

class UserLike(SQLModel, table=True):
    __tablename__ = "user_likes"
    user_id: UUID = Field(foreign_key="users.user_id", primary_key=True)
    track_id: UUID = Field(foreign_key="tracks.track_id", primary_key=True)
    liked_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="liked_tracks")
    track: "Track" = Relationship(back_populates="liked_by")

class ListeningHistory(SQLModel, table=True):
    __tablename__ = "listening_history"
    history_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id")
    track_id: UUID = Field(foreign_key="tracks.track_id")
    listened_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="listening_history")
    track: "Track" = Relationship(back_populates="in_history")