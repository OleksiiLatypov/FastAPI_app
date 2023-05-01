import asyncio
from pprint import pprint

from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.database.db import SessionLocal

database = SessionLocal()


async def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


if __name__ == '__main__':
    pprint(asyncio.run(get_user_by_email('mbullock@example.net', database)))
