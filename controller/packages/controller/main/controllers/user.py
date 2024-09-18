from http import HTTPStatus
from typing import Optional
from typing import Tuple

from passlib.handlers.pbkdf2 import pbkdf2_sha256

from controllers.base import Controller
from db.dao import UserDAO
from utils.jwt import generate_jwt


class UserController(Controller):
    ACTIONS = [
        'sign_up_user',
        'login_user'
    ]

    def _sign_up_user(self) -> Tuple[int, Optional[dict]]:
        """
        Registra un nuevo usuario.

        :return: Código de estado HTTP y datos de respuesta. En caso de éxito, se incluye el token JWT.
        """
        email = self.data.get('email')
        password = self.data.get('password')
        password_hash = pbkdf2_sha256.hash(password)
        user_dao = UserDAO()
        user = user_dao.create(email, password_hash)
        user_dao.close_session()

        if not user:
            return HTTPStatus.BAD_REQUEST, {'error': 'user_already_exists'}

        return HTTPStatus.CREATED, {
            'token': generate_jwt({'email': email, 'id': user.id}),
        }

    def _login_user(self) -> Tuple[int, Optional[dict]]:
        """
        Inicia sesión de un usuario.

        :return: Código de estado HTTP y datos de respuesta. En caso de éxito, se incluye el token JWT.
        """
        email = self.data.get('email')
        password = self.data.get('password')
        user_dao = UserDAO()
        user = user_dao.get_by_email(email)
        user_dao.close_session()

        if not user:
            return HTTPStatus.BAD_REQUEST, {'error': 'user_not_found'}

        if not pbkdf2_sha256.verify(password, user.password_hash):
            return HTTPStatus.BAD_REQUEST, {'error': 'invalid_password'}

        return HTTPStatus.OK, {
            'token': generate_jwt({'email': email, 'id': user.id}),
        }
