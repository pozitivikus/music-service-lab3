from sqlmodel import Session, select, func
from typing import Optional, List
from datetime import datetime, date
from models.user_models import User, UserLike, ListeningHistory
from models.music_models import Track, Artist, Album
import uuid

class UserRequests:
    @staticmethod
    def create_user(session: Session, email: str, password_hash: str, 
                   username: str, country_code: str = "RU") -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            username=username,
            country_code=country_code,
            subscription_type="free"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = session.exec(statement).first()
        return result
    
    @staticmethod
    def update_subscription(session: Session, user_id: uuid.UUID, 
                           subscription_type: str, expiry_date: date) -> Optional[User]:
        user = session.get(User, user_id)
        if user:
            user.subscription_type = subscription_type
            user.subscription_expiry = expiry_date
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
    
    @staticmethod
    def like_track(session: Session, user_id: uuid.UUID, track_id: uuid.UUID) -> UserLike:
        like = UserLike(user_id=user_id, track_id=track_id)
        session.add(like)
        session.commit()
        session.refresh(like)
        return like
    
    @staticmethod
    def unlike_track(session: Session, user_id: uuid.UUID, track_id: uuid.UUID) -> bool:
        statement = select(UserLike).where(
            UserLike.user_id == user_id,
            UserLike.track_id == track_id
        )
        like = session.exec(statement).first()
        if like:
            session.delete(like)
            session.commit()
            return True
        return False
    
    @staticmethod
    def add_to_listening_history(session: Session, user_id: uuid.UUID, 
                                track_id: uuid.UUID) -> ListeningHistory:
        history = ListeningHistory(user_id=user_id, track_id=track_id)
        session.add(history)
        session.commit()
        session.refresh(history)

        track = session.get(Track, track_id)
        if track:
            track.play_count += 1
            session.add(track)
            session.commit()
        return history
    
    @staticmethod
    def get_user_history(session: Session, user_id: uuid.UUID, 
                        limit: int = 50) -> List[ListeningHistory]:
        statement = (
            select(ListeningHistory)
            .where(ListeningHistory.user_id == user_id)
            .order_by(ListeningHistory.listened_at.desc())
            .limit(limit)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def get_top_users_by_listenings(session: Session, limit: int = 10) -> List:
        statement = (
            select(User.user_id, User.username, func.count(ListeningHistory.history_id).label("listen_count"))
            .join(ListeningHistory, User.user_id == ListeningHistory.user_id)
            .group_by(User.user_id, User.username)
            .order_by(func.count(ListeningHistory.history_id).desc())
            .limit(limit)
        )
        return session.exec(statement).all()