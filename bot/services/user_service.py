import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from shared.db import SessionLocal
from shared.models import User

logger = logging.getLogger(__name__)


def save_or_update_user(tg_user) -> User:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == tg_user.id).first()
        if user:
            user.username = tg_user.username
            user.first_name = tg_user.first_name
            user.last_name = tg_user.last_name
            logger.info("Updated user telegram_id=%d", tg_user.id)
        else:
            user = User(
                telegram_id=tg_user.id,
                username=tg_user.username,
                first_name=tg_user.first_name,
                last_name=tg_user.last_name,
            )
            db.add(user)
            logger.info("Created user telegram_id=%d", tg_user.id)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_users_count() -> int:
    db = SessionLocal()
    try:
        return db.query(User).count()
    finally:
        db.close()
