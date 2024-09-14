from typing import Optional

from sqlalchemy.exc import IntegrityError

from db.base import Session
from db.base import init_db
from db.models import User


class UserDAO:
    def __init__(self):
        init_db()
        self.session = Session()

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

    def close_session(self):
        """
        Cierra la sesión.
        """
        self.session.close()

    def commit(self):
        """
        Confirma los cambios en la sesión.
        """
        self.session.commit()
