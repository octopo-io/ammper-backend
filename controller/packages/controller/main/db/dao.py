from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.base import Session
from db.base import init_db
from db.models import User
from db.models import UserLinks


class DAO:
    def __init__(self):
        init_db()
        self.session = Session()

    def commit(self):
        self.session.commit()

    def close_session(self):
        self.session.close()


class LinkDAO(DAO):
    def create(self, user_id: int, link_id: str, institution: str) -> UserLinks:
        """
        Crea un nuevo enlace de usuario.

        :param user_id: ID del usuario.
        :param link_id: ID del enlace.
        :param institution: Institución del enlace.
        """
        self.session.add(UserLinks(user_id=user_id, link_id=link_id, institution=institution))
        self.commit()
        return self.get_by_institution_and_user_id(institution, user_id)

    def get_by_institution_and_user_id(self, institution: str, user_id: int) -> Optional[UserLinks]:
        """
        Obtiene un enlace por institución y usuario.

        :param institution: Institución del enlace.
        :param user_id: ID del usuario.
        :return: Enlace encontrado o None si no existe.
        """
        return self.session.query(UserLinks).filter_by(institution=institution, user_id=user_id).first()


class UserDAO(DAO):
    def create(self, email: str, password_hash: str) -> Optional[User]:
        """
        Crea un nuevo usuario.

        :param email: Email del usuario. Actúa como username.
        :param password_hash: Hash de la contraseña del usuario.
        :return: Usuario creado o None si ya existe un usuario con el mismo email.
        """
        try:
            user = User(email=email, password_hash=password_hash)
            self.session.add(user)
            self.commit()
            return self.get_by_email(email)
        except IntegrityError as e:  # Usuario existe
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por email.

        :param email: Email del usuario.
        :return: Usuario encontrado o None si no existe.
        """
        return self.session.query(User).filter_by(email=email).first()
