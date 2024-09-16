from typing import Union

import jwt
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from config import SECRET_KEY


def generate_jwt(data: dict) -> str:
    """
    Genera un token JWT con los datos proporcionados.

    :param data: Datos a incluir en el token.
    :return: Token JWT.
    """
    exp = datetime.now(timezone.utc) + timedelta(days=1)
    data['exp'] = exp
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')


def get_jwt_data(token: str) -> Union[dict, None]:
    """
    Obtiene los datos de un token JWT.

    :param token: Token JWT.
    :return: Datos del token o None si el token es inválido.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception:
        return None
