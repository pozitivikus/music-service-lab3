from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from typing import List
import uuid
from datetime import date
from decimal import Decimal

from database import get_session
from models.user_models import User
from models.music_models import Track, Artist, Album, Playlist
from models.subscription_models import SubscriptionPlan, Payment

from requests.user_requests import UserRequests
from requests.music_requests import MusicRequests
from requests.subscription_requests import SubscriptionRequests

app = FastAPI(title="Music Streaming Service API", version="1.0.0")

@app.post("/users/", response_model=User)
def create_user(email: str, password_hash: str, username: str, 
                country_code: str = "RU", session: Session = Depends(get_session)):
    user = UserRequests.get_user_by_email(session, email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserRequests.create_user(session, email, password_hash, username, country_code)

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: uuid.UUID, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/{user_id}/like/{track_id}")
def like_track(user_id: uuid.UUID, track_id: uuid.UUID, session: Session = Depends(get_session)):
    return UserRequests.like_track(session, user_id, track_id)

@app.get("/users/{user_id}/history")
def get_user_history(user_id: uuid.UUID, limit: int = 50, session: Session = Depends(get_session)):
    return UserRequests.get_user_history(session, user_id, limit)

@app.get("/search/tracks")
def search_tracks(query: str, limit: int = 20, session: Session = Depends(get_session)):
    return MusicRequests.search_tracks(session, query, limit)

@app.get("/search/artists")
def search_artists(query: str, limit: int = 20, session: Session = Depends(get_session)):
    return MusicRequests.search_artists(session, query, limit)

@app.get("/tracks/top")
def get_top_tracks(limit: int = 20, session: Session = Depends(get_session)):
    return MusicRequests.get_top_tracks(session, limit)

@app.get("/albums/{album_id}/tracks")
def get_album_tracks(album_id: uuid.UUID, session: Session = Depends(get_session)):
    return MusicRequests.get_album_tracks(session, album_id)

@app.post("/playlists/")
def create_playlist(title: str, created_by: uuid.UUID, description: str = None, 
                   is_public: bool = False, session: Session = Depends(get_session)):
    return MusicRequests.create_playlist(session, title, created_by, description, is_public)

@app.get("/subscription/plans", response_model=List[SubscriptionPlan])
def get_all_plans(session: Session = Depends(get_session)):
    return SubscriptionRequests.get_all_plans(session)

@app.post("/subscription/purchase")
def purchase_subscription(user_id: uuid.UUID, plan_id: uuid.UUID, 
                         external_payment_id: str = None, session: Session = Depends(get_session)):
    plan = session.get(SubscriptionPlan, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    payment = SubscriptionRequests.create_payment(
        session, user_id, plan_id, plan.price, "pending", external_payment_id
    )
    SubscriptionRequests.activate_premium(session, user_id, plan_id, payment.payment_id)
    return {"message": "Subscription activated", "payment_id": payment.payment_id}

@app.get("/analytics/revenue")
def get_revenue(start_date: date, end_date: date, session: Session = Depends(get_session)):
    revenue = SubscriptionRequests.get_revenue_by_period(session, start_date, end_date)
    return {"start_date": start_date, "end_date": end_date, "revenue": revenue}

@app.get("/statistics/top-users")
def get_top_users(limit: int = 10, session: Session = Depends(get_session)):
    return UserRequests.get_top_users_by_listenings(session, limit)

@app.get("/statistics/most-popular-plan")
def get_most_popular_plan(session: Session = Depends(get_session)):
    plan = SubscriptionRequests.get_most_popular_plan(session)
    return {"plan": plan}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)