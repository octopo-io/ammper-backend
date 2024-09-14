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
