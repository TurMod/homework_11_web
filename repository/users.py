from schemas import UserModel
from sqlalchemy.orm import Session

from db.models import User
from libgravatar import Gravatar

async def get_user_by_email(email: str, db: Session) -> User:
    """
    Gets user by email address.

    :param email: Email address.
    :type email: str
    :param db: Database session.
    :type db: Session
    :return: User.
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates new user.

    :param body: Data for contact.
    :type body: UserModel
    :param db: Database session.
    :type db: Session
    :return: Created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates refresh token for specific user.

    :param user: User for which token will update.
    :type user: User
    :param token: Refresh token.
    :type token: str | None
    :param db: Database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    Confirms email for specific user.

    :param email: Email address.
    :type email: str
    :param db: Database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email: str, url: str, db: Session) -> User:
    """
    Updates avatar for specific user.

    :param email: Email address.
    :type email: str
    :param url: Cloudinary URL address.
    :type url: str
    :param db: Database session.
    :type db: Session
    :return: Updated user.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
