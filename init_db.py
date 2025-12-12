from database import engine, create_db_and_tables
from sqlmodel import Session
from models.user_models import User
from models.music_models import Artist, Album, Track, Genre, ArtistGenre
from models.subscription_models import SubscriptionPlan
from requests.user_requests import UserRequests
from requests.music_requests import MusicRequests
from requests.subscription_requests import SubscriptionRequests
import uuid
from datetime import date, timedelta
from decimal import Decimal

def init_database():
    create_db_and_tables()
    with Session(engine) as session:
        free_plan = SubscriptionRequests.create_subscription_plan(
            session, "Free", Decimal('0'), "Бесплатный тариф с рекламой"
        )
        premium_plan = SubscriptionRequests.create_subscription_plan(
            session, "Premium", Decimal('299'), "Премиум без рекламы, скачивание треков"
        )
        family_plan = SubscriptionRequests.create_subscription_plan(
            session, "Family", Decimal('499'), "Семейная подписка для 6 человек"
        )

        genres_data = [
            ("Pop", "Поп-музыка"),
            ("Rock", "Рок-музыка"),
            ("Hip-Hop", "Хип-хоп и рэп"),
            ("Electronic", "Электронная музыка"),
            ("Jazz", "Джаз"),
            ("Classical", "Классическая музыка"),
            ("Metal", "Метал"),
            ("Indie", "Инди-музыка"),
        ]
        
        genres = {}
        for name, desc in genres_data:
            genre = Genre(name=name, description=desc)
            session.add(genre)
            session.commit()
            session.refresh(genre)
            genres[name] = genre

        users = []
        for i in range(1, 6):
            user = UserRequests.create_user(
                session,
                email=f"user{i}@example.com",
                password_hash=f"hash{i}",
                username=f"User{i}",
                country_code="RU"
            )
            users.append(user)

        artists_data = [
            ("The Weeknd", "Канадский певец", "CA", date(2010, 1, 1), ["Pop", "R&B"]),
            ("Imagine Dragons", "Американская поп-рок группа", "US", date(2008, 1, 1), ["Pop", "Rock", "Indie"]),
            ("Eminem", "Американский рэпер", "US", date(1996, 1, 1), ["Hip-Hop"]),
            ("Daft Punk", "Французский электронный дуэт", "FR", date(1993, 1, 1), ["Electronic"]),
            ("Queen", "Британская рок-группа", "UK", date(1970, 1, 1), ["Rock", "Pop"]),
        ]
        
        artists = []
        for name, desc, country, formed_date, genre_names in artists_data:
            artist = MusicRequests.create_artist(
                session, name, desc, country, formed_date
            )

            for genre_name in genre_names:
                if genre_name in genres:
                    artist_genre = ArtistGenre(
                        artist_id=artist.artist_id,
                        genre_id=genres[genre_name].genre_id
                    )
                    session.add(artist_genre)
            artists.append(artist)
            session.commit()

        albums_data = [
            ("After Hours", artists[0].artist_id, date(2020, 3, 20)),
            ("Starboy", artists[0].artist_id, date(2016, 11, 25)),
            ("Night Visions", artists[1].artist_id, date(2012, 9, 4)),
            ("The Eminem Show", artists[2].artist_id, date(2002, 5, 26)),
            ("Random Access Memories", artists[3].artist_id, date(2013, 5, 17)),
            ("A Night at the Opera", artists[4].artist_id, date(1975, 11, 21)),
        ]
        
        albums = []
        for title, artist_id, release_date in albums_data:
            album = MusicRequests.create_album(session, title, artist_id, release_date)
            albums.append(album)

        tracks_data = [
            ("Blinding Lights", 200, albums[0].album_id, 1),
            ("Save Your Tears", 215, albums[0].album_id, 2),
            ("Starboy", 230, albums[1].album_id, 1),
            ("Radioactive", 187, albums[2].album_id, 1),
            ("Demons", 177, albums[2].album_id, 2),
            ("Without Me", 290, albums[3].album_id, 1),
            ("Lose Yourself", 326, None, None),
            ("Get Lucky", 369, albums[4].album_id, 1),
            ("Bohemian Rhapsody", 354, albums[5].album_id, 1),
            ("We Will Rock You", 122, albums[5].album_id, 2),
        ]
        
        tracks = []
        for title, duration, album_id, track_num in tracks_data:
            track = MusicRequests.create_track(
                session, title, duration, f"/tracks/{title.lower().replace(' ', '_')}.mp3",
                album_id, track_num
            )
            tracks.append(track)

        playlist1 = MusicRequests.create_playlist(
            session, "Мой топ 2024", users[0].user_id,
            "Лучшие треки 2024 года", True
        )
        
        playlist2 = MusicRequests.create_playlist(
            session, "Для тренировки", users[1].user_id,
            "Энергичная музыка для спорта", True
        )

        for i in range(3):
            MusicRequests.add_track_to_playlist(
                session, playlist1.playlist_id,
                tracks[i].track_id, users[0].user_id
            )
        
        for i in range(3, 6):
            MusicRequests.add_track_to_playlist(
                session, playlist2.playlist_id,
                tracks[i].track_id, users[1].user_id
            )

        for user in users[:3]:
            for track in tracks[:5]:
                UserRequests.add_to_listening_history(session, user.user_id, track.track_id)

        for i, track in enumerate(tracks[:7]):
            user_idx = i % len(users)
            UserRequests.like_track(session, users[user_idx].user_id, track.track_id)
        
        premium_user = users[0]
        payment = SubscriptionRequests.create_payment(
            session, premium_user.user_id, premium_plan.plan_id,
            premium_plan.price, "completed", "ext_12345"
        )
        SubscriptionRequests.activate_premium(
            session, premium_user.user_id, premium_plan.plan_id, payment.payment_id
        )
        
        session.commit()
        print("База данных успешно инициализирована!")
        print(f"Создано: {len(users)} пользователей, {len(artists)} исполнителей,")
        print(f"{len(albums)} альбомов, {len(tracks)} треков")

if __name__ == "__main__":
    init_database()