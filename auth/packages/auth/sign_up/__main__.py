from http import HTTPStatus

from db.models import User
from db.base import Session
from db.base import init_db

init_db()


def main(args: dict, context: object) -> dict:
    if args.get('http', {}).get('method') != 'POST':
        return {'statusCode': HTTPStatus.METHOD_NOT_ALLOWED}

    email = args.get('email')
    password = args.get('password')
    user = User(email=email, password_hash=password)
    session = Session()
    session.add(user)
    session.commit()
    session.close()

    return {
        'body': {
            'message': 'Test',
            'email': email,
            'password': password
        },
        'statusCode': 200
    }
