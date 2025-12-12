from sqlmodel import Session, select, func, or_
from typing import Optional, List, Tuple
from datetime import date
from models.music_models import Track, Artist, Album, Playlist, PlaylistTrack, Genre, ArtistGenre
from models.user_models import User
import uuid

class MusicRequests:
    @staticmethod
    def create_track(session: Session, title: str, duration: int, file_url: str,
                    album_id: Optional[uuid.UUID] = None, track_number: Optional[int] = None) -> Track:
        track = Track(
            title=title,
            duration=duration,
            file_url=file_url,
            album_id=album_id,
            track_number=track_number
        )
        session.add(track)
        session.commit()
        session.refresh(track)
        return track
    
    @staticmethod
    def create_artist(session: Session, name: str, description: Optional[str] = None,
                     country_code: str = "US", date_formed: Optional[date] = None) -> Artist:
        artist = Artist(
            name=name,
            description=description,
            country_code=country_code,
            date_formed=date_formed
        )
        session.add(artist)
        session.commit()
        session.refresh(artist)
        return artist
    
    @staticmethod
    def create_album(session: Session, title: str, artist_id: uuid.UUID,
                    release_date: Optional[date] = None) -> Album:
        album = Album(
            title=title,
            artist_id=artist_id,
            release_date=release_date
        )
        session.add(album)
        session.commit()
        session.refresh(album)
        return album
    
    @staticmethod
    def search_tracks(session: Session, query: str, limit: int = 20) -> List[Track]:
        statement = (
            select(Track)
            .where(Track.title.ilike(f"%{query}%"))
            .limit(limit)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def search_artists(session: Session, query: str, limit: int = 20) -> List[Artist]:
        statement = (
            select(Artist)
            .where(Artist.name.ilike(f"%{query}%"))
            .limit(limit)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def get_album_tracks(session: Session, album_id: uuid.UUID) -> List[Track]:
        statement = (
            select(Track)
            .where(Track.album_id == album_id)
            .order_by(Track.track_number)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def get_top_tracks(session: Session, limit: int = 20) -> List[Track]:
        statement = (
            select(Track)
            .order_by(Track.play_count.desc())
            .limit(limit)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def create_playlist(session: Session, title: str, created_by: uuid.UUID,
                       description: Optional[str] = None, is_public: bool = False) -> Playlist:
        playlist = Playlist(
            title=title,
            description=description,
            is_public=is_public,
            created_by=created_by
        )
        session.add(playlist)
        session.commit()
        session.refresh(playlist)
        return playlist
    
    @staticmethod
    def add_track_to_playlist(session: Session, playlist_id: uuid.UUID,
                             track_id: uuid.UUID, added_by: uuid.UUID) -> PlaylistTrack:
        playlist_track = PlaylistTrack(
            playlist_id=playlist_id,
            track_id=track_id,
            added_by=added_by
        )
        session.add(playlist_track)
        session.commit()
        session.refresh(playlist_track)
        return playlist_track
    
    @staticmethod
    def get_playlist_tracks(session: Session, playlist_id: uuid.UUID) -> List[Tuple[Track, PlaylistTrack]]:
        statement = (
            select(Track, PlaylistTrack)
            .join(PlaylistTrack, Track.track_id == PlaylistTrack.track_id)
            .where(PlaylistTrack.playlist_id == playlist_id)
            .order_by(PlaylistTrack.added_at)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def get_artist_discography(session: Session, artist_id: uuid.UUID) -> List[Album]:
        statement = (
            select(Album)
            .where(Album.artist_id == artist_id)
            .order_by(Album.release_date.desc())
        )
        return session.exec(statement).all()
    
    @staticmethod
    def get_tracks_by_genre(session: Session, genre_name: str, limit: int = 50) -> List[Track]:
        statement = (
            select(Track)
            .join(Album, Track.album_id == Album.album_id)
            .join(Artist, Album.artist_id == Artist.artist_id)
            .join(ArtistGenre, Artist.artist_id == ArtistGenre.artist_id)
            .join(Genre, ArtistGenre.genre_id == Genre.genre_id)
            .where(Genre.name.ilike(f"%{genre_name}%"))
            .limit(limit)
        )
        return session.exec(statement).all()