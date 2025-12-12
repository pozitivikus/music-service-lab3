from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID, uuid4

class Genre(SQLModel, table=True):
    __tablename__ = "genres"
    genre_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(unique=True, index=True, max_length=100)
    description: Optional[str] = Field(default=None)
    artists: List["ArtistGenre"] = Relationship(back_populates="genre")

class Artist(SQLModel, table=True):
    __tablename__ = "artists"
    artist_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None)
    country_code: Optional[str] = Field(default=None, max_length=2)
    date_formed: Optional[date] = Field(default=None)
    photo_url: Optional[str] = Field(default=None, max_length=500)
    genres: List["ArtistGenre"] = Relationship(back_populates="artist")
    albums: List["Album"] = Relationship(back_populates="artist")

class ArtistGenre(SQLModel, table=True):
    __tablename__ = "artist_genres"
    artist_id: UUID = Field(foreign_key="artists.artist_id", primary_key=True)
    genre_id: UUID = Field(foreign_key="genres.genre_id", primary_key=True)
    artist: Artist = Relationship(back_populates="genres")
    genre: Genre = Relationship(back_populates="artists")

class Album(SQLModel, table=True):
    __tablename__ = "albums"
    album_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    artist_id: UUID = Field(foreign_key="artists.artist_id")
    release_date: Optional[date] = Field(default=None)
    cover_art_url: Optional[str] = Field(default=None, max_length=500)
    artist: Artist = Relationship(back_populates="albums")
    tracks: List["Track"] = Relationship(back_populates="album")

class Track(SQLModel, table=True):
    __tablename__ = "tracks"
    track_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    duration: int = Field(gt=0) 
    file_url: str = Field(max_length=500)
    album_id: Optional[UUID] = Field(default=None, foreign_key="albums.album_id")
    track_number: Optional[int] = Field(default=None)
    play_count: int = Field(default=0)
    album: Optional[Album] = Relationship(back_populates="tracks")
    liked_by: List["UserLike"] = Relationship(back_populates="track")
    in_history: List["ListeningHistory"] = Relationship(back_populates="track")
    in_playlists: List["PlaylistTrack"] = Relationship(back_populates="track")

class Playlist(SQLModel, table=True):
    __tablename__ = "playlists"
    playlist_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None)
    is_public: bool = Field(default=False)
    created_by: UUID = Field(foreign_key="users.user_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cover_image_url: Optional[str] = Field(default=None, max_length=500)
    creator: "User" = Relationship(back_populates="playlists")
    tracks: List["PlaylistTrack"] = Relationship(back_populates="playlist")

class PlaylistTrack(SQLModel, table=True):
    __tablename__ = "playlist_tracks"
    playlist_id: UUID = Field(foreign_key="playlists.playlist_id", primary_key=True)
    track_id: UUID = Field(foreign_key="tracks.track_id", primary_key=True)
    added_at: datetime = Field(default_factory=datetime.utcnow)
    added_by: UUID = Field(foreign_key="users.user_id")
    playlist: Playlist = Relationship(back_populates="tracks")
    track: Track = Relationship(back_populates="in_playlists")